from easygraphics.processing import ProcessingWidget
from easygraphics.image import Image
import easygraphics
import inspect

image_funcs = dir(Image)
for func in easygraphics.__all__:
    if not func in image_funcs:
        continue
    if func.startswith("_"):
        continue
    fun = eval(f"easygraphics.{func}")
    if not callable(fun):
        continue
    sig = inspect.signature(fun)
    parameters = []
    for param in sig.parameters:
        if param != 'self':
            if param == 'args':
                parameters.append('*args')
            elif param == 'kwargs':
                parameters.append('**kwargs')
            else:
                parameters.append(param)
    print(f"def {func}{sig}:")
    if sig.return_annotation is not inspect.Signature.empty:
        print(f"    return _widget.get_canvas().{func}({','.join(parameters)})")
    else:
        print(f"    _widget.get_canvas().{func}({','.join(parameters)})")
    print("")
