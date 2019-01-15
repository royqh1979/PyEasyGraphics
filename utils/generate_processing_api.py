from easygraphics import Image
import inspect

for func in dir(Image):
    if func.startswith("_"):
        continue
    sig = inspect.signature(eval(f"Image.{func}"))
    if not 'self' in sig.parameters.keys():
        continue
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
        print(f"    return self._image.{func}({','.join(parameters)})")
    else:
        print(f"    self._image.{func}({','.join(parameters)})")
    print("")
