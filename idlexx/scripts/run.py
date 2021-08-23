import imp
imp.load_package('pkg', '../__init__.py').run()

# another way
# import importlib
# spec = importlib._bootstrap_external.spec_from_file_location('pkg', '../__init__.py')
# pkg  = importlib._bootstrap._load(spec)
# pkg.run()

# another way
# import importlib.util
# spec = importlib.util.spec_from_file_location('pkg', '../__init__.py')
# pkg = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(pkg)
# pkg.run()
