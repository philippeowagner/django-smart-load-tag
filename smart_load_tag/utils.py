from django.template import Library, TemplateSyntaxError, InvalidTemplateLibrary, get_templatetags_modules, import_library

def load(parser, lib, tag='*', name=None, namespace=None, app=None):
    try:
        lib_name = lib
        lib = Library()
        module_lib = get_library(lib_name, app)
        lib.tags.update(module_lib.tags)
        lib.filters.update(module_lib.filters)
        if tag != '*':
            lib.tags = {tag: lib.tags[tag]}
        if name:
            for tag in lib.tags.keys():
                lib.tags[name] = lib.tags[tag]
                if tag != name:
                    del lib.tags[tag]
        if namespace:
            for tag in lib.tags.keys():
                lib.tags['%s.%s' % (namespace, tag)] = lib.tags[tag]
                del lib.tags[tag]
        parser.add_library(lib)
    except InvalidTemplateLibrary, e:
        raise TemplateSyntaxError("'%s' is not a valid tag library: %s" % (lib, e))

def get_library(library_name, app_name=None):
    templatetags_modules = get_templatetags_modules()
    tried_modules = []
    for module in templatetags_modules:
        taglib_module = '%s.%s' % (module, library_name)
        tried_modules.append(taglib_module)
        lib = import_library(taglib_module)
        if lib and app_name and taglib_module.split('.')[-3] == app_name:
            break
    if not lib:
        raise InvalidTemplateLibrary("Template library %s not found, tried %s" % (library_name, ','.join(tried_modules)))

    return lib
