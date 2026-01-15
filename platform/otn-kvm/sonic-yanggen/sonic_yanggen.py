import sys
import libyang as ly
from typing import Optional
import datetime


DEBUG_ENABLE = False
MATCH_WARNING = True
MODEL_TITLE_SRC = 'openconfig'
MODEL_TITLE_DEST = 'sonic'
ANNOTATION_SUFFIX = '-annot'
YANG_SUFFIX = '.yang'
DB_TYPE_CONFIG = 'config'
DB_TYPE_STATE = 'state'
DB_NAMES = {DB_TYPE_CONFIG: 'CONFIG_DB', DB_TYPE_STATE: 'STATE_DB'}


""" table array index define """
TB_PATH_IDX     = 0
TB_NAME_IDX     = 1
TB_DBTYPE_IDX   = 2
TB_DBNAME_IDX   = 3
TB_KEY_IDX      = 4
TB_FIELD_IDX    = 5

""" key or field index define """
KEY_PATH_IDX    = 0
KEY_DEFINE_IDX  = 1
KEY_ISNAME_IDX  = 2


class Annotation:
    """
    Parse annotation yang file
    """

    def __init__(self, search_path, yang_file) -> None:
        self.search_path = search_path
        self.yang_file = yang_file
        self.info = {}
        self.tables = []
        self.dbs = set()
        self.parse()


    def leaf_value(self, content, key) -> Optional[str]:
        """
        Parse the deviate adding value
        """
        pos = content.find(key)
        if pos == -1:
            return None

        pos1 = content.find('"', pos) + 1
        pos2 = content.find('"', pos1)
        return content[pos1:pos2].strip()


    def key_xpath(self, deviation, key) -> Optional[list]:
        """
        Parse the deviation xpath
        """
        field_name = self.leaf_value(deviation, key)
        if field_name is None:
            return None
        
        xpath = deviation[:deviation.find('{')].strip()[1:-1]

        # restore the prefix name with module name
        xpath = xpath.replace(self.info['src_module'][1], self.info['src_module'][0])
        for imp in self.info['imports']:
            xpath = xpath.replace(imp[1], imp[0])

        return [xpath, field_name]


    def table_name(self, deviation) -> None:
        """
        Parse the table name, and add extra definition for table structure.
        """
        table_name = self.leaf_value(deviation, 'sonic-ext:table-name')
        if table_name is None:
            return

        xpath = self.key_xpath(deviation, 'sonic-ext:table-name')[0]

        db_name = self.leaf_value(deviation, 'sonic-ext:db-name')
        if db_name is None or db_name == DB_NAMES[DB_TYPE_CONFIG]:
            self.dbs.add(DB_TYPE_CONFIG)
            self.tables.append([xpath, table_name, DB_TYPE_CONFIG, DB_NAMES[DB_TYPE_CONFIG], None, []])
        elif db_name == DB_NAMES[DB_TYPE_STATE]:
            self.dbs.add(DB_TYPE_STATE)
            self.tables.append([xpath, table_name, DB_TYPE_STATE, db_name, None, []])
        else:
            raise Exception("Not support the db name " + db_name)

        return


    def key_name(self, deviation) -> None:
        """
        Parse key name or key transformer
        """
        if len(self.tables) < 1:
            return

        v = self.key_xpath(deviation, 'sonic-ext:key-name')
        if v is not None:
            v.append(True)
            self.tables[-1][TB_KEY_IDX] = v
            return

        v = self.key_xpath(deviation, 'sonic-ext:key-transformer')
        if v is None:
            return

        v.append(False)
        self.tables[-1][TB_KEY_IDX] = v


    def field_name(self, deviation) -> None:
        """
        Parse field name or field transformer
        """
        if len(self.tables) < 1:
            return

        v = self.key_xpath(deviation, 'sonic-ext:field-name')
        if v is not None:
            v.append(True)
            self.tables[-1][TB_FIELD_IDX].append(v)
            return


        v = self.key_xpath(deviation, 'sonic-ext:field-transformer')
        if v is None:
            return

        v.append(False)
        self.tables[-1][TB_FIELD_IDX].append(v)


    def parse(self) -> None:
        """
        Examples for arguments:
        info: list, eg. {'src_module': [yang module name, yang module prefix], 'imports': [[yang module name, yang module prefix], ...]}
        tables: array, eg. [[xpath, table name, table type, db type], ...]
        fields: array, eg. [[[xpath, field name], ...], ...]
        keys: array, eg. [xpath, ...]
        """
        imports = []
        ctx = ly.Context(self.search_path, leafref_extended=True)
        module = ctx.load_module(self.yang_file)
        module_name = module.name()
        for imp in module.imports():
            """
            TODO
            Need a better way to find the original openconfig module name.
            """
            if imp.name() + ANNOTATION_SUFFIX ==  module_name:
                self.info['src_module'] = [imp.name(), imp.prefix()]
            else:
                imports.append([imp.name(), imp.prefix()])
        self.info['imports'] = imports

        debug_print(self.info)

        content = module.print('yang', ly.IOType.MEMORY)
        deviations = content.split(' deviation ')
        for deviation in deviations[1:]:
            deviation = deviation.strip()
            self.table_name(deviation)
            self.key_name(deviation)
            self.field_name(deviation)
        '''
        # determin the order relationship by table name
        table_count = len(self.tables)
        for i in range(table_count):
            children = []
            for j in range(table_count):
                if j == i:
                    continue
                if self.tables[j][0].find(self.tables[i][0]) == 0:
                    children.append(j)

            self.tables[i].append(children)
        '''


        debug_print('tables---------------------------------------------------------------')
        debug_print(self.tables)
        debug_print('---------------------------------------------------------------------')


class Generator:
    """
    Generate sonic yang file by annotation and open-config yang files.
    """

    def __init__(self, search_path, annot, cfg) -> None:
        self.search_path = search_path
        self.annot = annot
        self.cfg = cfg
        self.ctx = ly.Context(search_path, leafref_extended=True)
        self.module = self.__load_module()
        self.module_name = self.__name()
        self.field_record = []


    def __load_module(self) -> ly.Module:
        for m in self.annot.info['imports']:
            self.ctx.load_module(m[0])

        return self.ctx.load_module(self.annot.info['src_module'][0])


    def __match_warning(self, xpath, in_name, out_name) -> None:
        if MATCH_WARNING:
            print('\033[93m*Can not generate [' + xpath + '], which is defined in [' + in_name + '], use [' + out_name + '] as default.\033[0m')

    
    def __name(self) -> str:
        name = self.module.name()
        if MODEL_TITLE_SRC not in name:
            raise Exception("Failed to tranform module name. Invalid tranform key: " + MODEL_TITLE_SRC)

        return name.replace(MODEL_TITLE_SRC, MODEL_TITLE_DEST)


    def __to_words(self, xpath) -> str:
        xpath = xpath.replace(self.module.name() + ':', '')
        return xpath[1:xpath.find('/', 1)].replace('-', ' ')


    def __find_field(self, fields, key) -> bool:
        if len(key) == 0:
            return True

        if len(fields) == 0:
            return False

        for field in fields:
            xpath = field[0]
            xpath = xpath[xpath.rfind('/')+1:]
            xpath = xpath.replace(self.module.name() + ':', '')
            if key == xpath:
                return True

        return False


    def namespace(self) -> str:
        """
        Generate namespace for sonic yang
        """
        return 'namespace "http://github.com/Azure/' + self.module_name + '";'


    def prefix(self, title) -> str:
        """
        Generate prefix for sonic yang
        """
        prefix = 'prefix '
        words = self.module_name.split('-')

        for wd in words:
            if wd == title:
                prefix += wd
            else:
                prefix += '-'
                prefix += wd[:3]

        prefix += ';'

        return prefix


    def imports(self) -> str:
        """
        Generate imports information for sonic yang
        """
        return 'import sonic-extension { prefix sonic-ext; }'


    def organization(self) -> str:
        """
        Generate organization information for sonic yang
        """
        return 'organization "SONiC";'


    def contact(self) -> str:
        """
        Generate contact information for sonic yang
        """
        return 'contact "SONiC";'


    def description(self) -> str:
        """
        Generate description for sonic yang
        """
        return 'description "' + self.module_name.replace('-', ' ').upper() + '";'


    def revision(self) -> str:
        """
        Generate revision for sonic yang
        """
        return 'revision ' + datetime.date.today().strftime('%Y-%m-%d') + '{ description "Initial revision.";}'


    def gen_type(self, type) -> str:
        """
        Generate leaf type for sonic yang
        """
        text = ''
        if type is None:
            return text

        text = 'type '
        is_simple = True

        if type.base() is ly.Type.UNION:
            is_simple = False
            text += type.basename() + '{'
            for utype in type.union_types():
                text += self.gen_type(utype)
            text += '}'
        elif type.base() in ly.Type.STR_TYPES:
            text += ly.Type.BASENAMES[ly.Type.STRING]
        elif type.leafref_type() is not None:
            text += type.leafref_type().basename()
        else:
            text += type.basename()

        # other child types processing
        fraction_digits = type.fraction_digits()
        range = type.range()
        if fraction_digits is not None or range is not None:
            is_simple = False
            text += '{'

            if fraction_digits is not None:
                text += 'fraction-digits ' + str(fraction_digits) + ';'
            if range :
                text += 'range "' + range + '";'

            text += '}'

        if is_simple:
            text += ';'

        return text


    def gen_unit(self, node) -> str:
        """
        Generate leaf unit for sonic yang
        """
        text = ''

        if hasattr(node, 'units') and node.units() is not None:
            text += 'units ' + node.units() + ';'

        return text


    def gen_key(self, table, key_info) -> str:
        """
        Generate list key information for sonic yang
        """
        debug_print('key info:')
        debug_print(key_info)

        node = next(self.ctx.find_path(key_info[KEY_PATH_IDX]))

        keys = []
        text = 'key "'

        if not hasattr(node, 'keys'):
            node = node.parent()

        if any(node.keys()):
            for key in node.keys():
                key_name = key.name()
                keys.append(key_name)
                if key_info[KEY_ISNAME_IDX]:
                    text += key_info[KEY_DEFINE_IDX]
                else:
                    text += key_name
                text += ' '
            text = text.strip()
            text += '";'
        else:
            text += key_info[KEY_DEFINE_IDX] + '";'

        # special case processing, insert key leaf when no filed defined
        for key in keys:
            if not self.__find_field(table[TB_FIELD_IDX], key):
                field = [key_info[KEY_PATH_IDX] + '/' + key, key, True]
                text += self.gen_leaf(table, field)

            # warning for replacing
            if not key_info[KEY_ISNAME_IDX]:
                self.__match_warning(key_info[KEY_PATH_IDX], key_info[KEY_DEFINE_IDX], key)

        return text


    def gen_leaf(self, table, field_info) -> str:
        """
        Generate leaf information for sonic yang
        """
        debug_print('field info:')
        debug_print(field_info)

        node = next(self.ctx.find_path(field_info[KEY_PATH_IDX]))
        node_name = node.name()
 
        # leaf name
        ''' use default field name or annotation name '''
        key = field_info[KEY_DEFINE_IDX] if field_info[KEY_ISNAME_IDX] else node_name

        # Check if the key value is duplicated
        if key in self.field_record:
            key += '-'
            key += DB_TYPE_CONFIG if field_info[KEY_PATH_IDX].rfind(DB_TYPE_STATE) == -1 else DB_TYPE_STATE

        text = 'leaf ' + key + ' {'
        # leaf description
        text += 'description "' + (node.parent().description() if key == 'instant' else node.description()) + '";'
        # leaf basic type
        text += self.gen_type(node.type())
        # leaf units
        text += self.gen_unit(node)

        text += '}'

        # record the history field
        self.field_record.append(key)

        # warning for replacing
        if not field_info[KEY_ISNAME_IDX]:
            self.__match_warning(field_info[KEY_PATH_IDX], field_info[KEY_DEFINE_IDX], key)

        return text


    def gen_list(self, table) -> str:
        """
        Generate list information for sonic yang
        """
        text = ''

        # list key
        text += self.gen_key(table, table[TB_KEY_IDX])

        self.field_record.clear()
        for field in table[TB_FIELD_IDX]:
            text += self.gen_leaf(table, field)

        return text


    def gen_container(self, table) -> str:
        """
        Generate container information for sonic yang
        """
        text = 'container ' + table[TB_NAME_IDX] + ' {'
        # config
        if table[TB_DBTYPE_IDX] == DB_TYPE_CONFIG:
            text += 'sonic-ext:db-name "' + table[TB_DBNAME_IDX] + '";'
        # state
        else:
            text += 'config false;sonic-ext:db-name "' + table[TB_DBNAME_IDX] + '";'

        node = next(self.ctx.find_path(table[TB_PATH_IDX]))
        text += 'description "' + node.description() + '";'
        text += 'list ' + table[TB_NAME_IDX] + '_LIST {'

        text += self.gen_list(table)

        text += '}}'

        return text


    def gen_head(self) -> str:
        """
        Generate header information for sonic yang
        """
        text = 'module ' + self.module_name + ' {'
        text += self.namespace()
        text += self.prefix(MODEL_TITLE_DEST)
        text += self.imports()
        text += self.organization()
        text += self.contact()
        text += self.description()
        text += self.revision()
        text += 'container ' + self.module_name + '{'

        return text


    def gen_tables(self) -> str:
        """
        Generate table information for sonic yang
        """
        text = ''

        for table in self.annot.tables:
            if self.cfg is None or table[TB_DBTYPE_IDX] == self.cfg:
                text += self.gen_container(table)

        text += '}}'

        return text
    

    def gen_yang(self) -> str:
        """
        Generate sonic yang
        """
        text = self.gen_head()
        text += self.gen_tables()

        debug_print(text)
        return text


def to_file(search_path, module_name, yang, out_dir) -> str:
    """
    Write yang context to file
    """
    ctx = ly.Context(search_path)
    module = ctx.parse_module_str(yang)
    text = module.print("yang", ly.IOType.MEMORY)

    debug_print(text)

    path = out_dir.strip()
    if path[-1] != '/':
        path += '/'
    path += module_name + YANG_SUFFIX

    with open(path, 'w') as f:
        f.write(text)

    return path


def debug_print(data):
    if DEBUG_ENABLE:
        print(data)


def sonic_yangload(search_path, yang_file, out_dir) -> list:
    """
    Directly load sonic yang model, skip generation for sonic annotation yang model.
    """
    ctx = ly.Context(search_path, leafref_extended=True)
    module = ctx.load_module(yang_file)
    module_name = module.name()
    text = module.print('yang', ly.IOType.MEMORY)
    path = to_file(search_path, module_name, text, out_dir)

    print('sonic_yangload', path)

    # return module name and yang text content for extension
    return {'name': module_name, 'type': None, 'yang': text.replace('\n', '')}


def sonic_yanggen(search_path, module_name, out_dir, sel_db = None) -> list:
    """
    Automatically generate a sonic annotation yang model to a sonic yang model.

    Inputs:
    search_path: mandatory, yang model search directory, including annotation yang model and dependency models.
    module_name: mandatory, module name of annotation yang file or sonic yang file
    out_dir: mandatory, output directory for target sonic yang model.
    sel_db: optional, None|config|state db selection, default is None selection generating all

    Return: list value or None.
    Example:
    {'name': 'xxxxx', 'type': 'config/state', 'yang': 'xxxxx'}

    """

    # 1. check the module need to tranform or not
    if ANNOTATION_SUFFIX not in module_name:
        return sonic_yangload(search_path, module_name, out_dir)

    # 2. parse the annotation yang file
    annot = Annotation(search_path, module_name)

    # 3. create yang text by source module
    gen = Generator(search_path, annot, sel_db)
    text = gen.gen_yang()

    # 4. format yang text and output file
    path = to_file(search_path, gen.module_name, text, out_dir)

    print('sonic_yanggen', path)

    # return module name and yang text content for extension
    return {'name': gen.module_name, 'type': sel_db, 'yang': text.replace('\n', '')}


def main(argv):
    """
    argv[1]: mandatory, yang model search directory
    argv[2]: mandatory, module name of annotation yang file or sonic yang file
    argv[3]: mandatory, output directory for generation file
    argv[4]: optional, None|config|state db selection, default is None selection generating all
    """

    sonic_yanggen(argv[1], argv[2], argv[3], argv[4] if len(argv) > 4 else None)

    # examples
    #sonic_yanggen('/home/sonic/sonic/sonic-buildimage/src/sonic-mgmt-common/models/yang', 'openconfig-optical-attenuator-annot', '/home/sonic/work/test')
    #sonic_yanggen('/home/sonic/sonic/sonic-buildimage/src/sonic-mgmt-common/models/yang', 'openconfig-optical-amplifier-annot', '/home/sonic/work/test')


if __name__ == "__main__":
    main(sys.argv)
