import time


def timer(foo, *args, **kwargs):
    def inner(*args, **kwargs):
        start = time.time()
        retorno = foo(*args, **kwargs)
        end = time.time()
        print(f"Tempo de execução da {foo.__name__}: {end - start}")
        return retorno
    return inner