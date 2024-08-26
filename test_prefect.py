from prefect import flow, task

@task(log_prints=True)
def add(x, y):
    return x + y

@task(log_prints=True)
def multiply(x, y):
    return x * y

@flow(log_prints=True)
def main():
    a = add(1, 2)
    b = multiply(a, 3)
    print(a)

main()