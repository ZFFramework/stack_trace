project('stack_trace')

# Variables
flags = cfgvar('stack_trace.flags', 'flags', description='list of abstract build flags (see doozer docs)')
platform = cfgvar('stack_trace.platform', description='"windows" or "osx"')


# Builds a static library for stack_trace.
@target
def staticlib(kit):
    opt = kit.cpp.opt(*flags)
    opt.sources += here/'src/*.cpp'
    opt.includes += [here/'include']

    syslibs = []

    if platform == 'windows':
        if 'msvc' in kit.installed():
            opt.cppflags -= ['/Za']

        syslibs = ['imagehlp']

        if 'gpp' in kit.installed():
            syslibs += ['bfd', 'iberty']
            if kit.cpp.compiler.version >= (4,5):
                syslibs += ['intl', 'iconv']

    return properties(
        libs = [kit.cpp.lib('stack_trace', opt)],
        includes = [here/'include'],
        syslibs = syslibs
    )

@target
def basic_example(kit):
    stack_trace = staticlib(kit)

    opt = kit.cpp.opt(*flags)

    opt.sources += here/'example/*.cpp'
    opt.includes += stack_trace.includes
    opt.libs += stack_trace.libs
    opt.syslibs += stack_trace.syslibs

    return process(kit.cpp.exe('example', opt))

@target
def examples(kit):
    return [basic_example(kit)]

@target
def default(kit):
    examples(kit)
