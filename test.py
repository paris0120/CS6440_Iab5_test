import json
import os


def test():
    solution_path = 'output'
    test = 0
    errors = []
    for runner in ['CMS125v11Runner', 'CMS147v11Runner', 'CMS165v11Runner']:
        for file in os.listdir(os.path.join(solution_path, runner)):
            test+=1
            solution = os.path.join(solution_path, runner, file)
            output = os.path.join('test_subset', solution_path, runner, file)
            if(os.path.exists(output)):
                with open(solution) as s, open(output) as o:
                    if (json.load(o) != json.load(s)):
                        errors.append(output)
                        print(output, ': error detected.')
            else:
                errors.add(output)
                print(output, 'is missing.')
    print(test, 'files were tested.')
    if(len(errors)>0):
        print(len(errors), 'errors were found:', errors)
    else:
        print('All tests were passed.')
            
         

if __name__ == "__main__":
    test()