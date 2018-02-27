from bottle import run, post

import classwork.verifier


@post('/<org>/<assignment_name>/verify')
def verify_assignment(org, assignment_name):
    verifier = classwork.verifier.Verifier()
    verifier.verify_assignment(org, assignment_name)


run(host='localhost', port=8080)
