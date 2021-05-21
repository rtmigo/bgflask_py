import chkpkg


if __name__ == "__main__":
    with chkpkg.Package() as p:
        p.run_python_code('from runwerk import RunWerk')

