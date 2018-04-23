def combine(files_in, file_out):
    with open(file_out, 'w') as f_out:
        for f_in in files_in:
            with open(f_in) as f:
                for line in f:
                    f_out.write(line)
