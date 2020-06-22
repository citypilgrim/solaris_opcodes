# imports
from .decorators import *
from .params import *

# main func


@verbose
@announcer
def f2():
    pass

@verbose
@announcer
def f1():
    f2(verbboo=True)

@verbose
@announcer
def main():
    f1(verbboo=False)


# running
if __name__ == '__main__':
    main(verbboo=True)
