class Call:
    def __init__(self, op):
        self._op = op
        self._operand = []

    def __call__(self, *n):
        self._operand.extend(list(n))
        return self

    def print_graph(self, done=None):
        if done is None:
            done = {}

        if self not in done:
            args = []
            for n in self._operand:
                args.append(n.print_graph(done))
            done[self] = len(done) + 1
            print(f"%{done[self]} = {self._op}({','.join([str(item) for item in args])})")
        return done[self]

def op_commoning(call):
    call_map = {}
    _collect_calls(call, call_map)
    return _reconstruct(call, call_map)

def _collect_calls(call, call_map):
    if call._op in call_map:
        call_map[call._op].append(call)
    else:
        call_map[call._op] = [call]
    for operand in call._operand:
        _collect_calls(operand, call_map)

def _reconstruct(call, call_map):
    if call._op in call_map and len(call_map[call._op]) > 1:
        return call_map[call._op][0]
    else:
        operands = [_reconstruct(operand, call_map) for operand in call._operand]
        return Call(call._op)(*operands)

if __name__ == "__main__":
    input_call = Call("I")
    c = Call("C")(Call("B")(Call("A")(input_call)))
    d = Call("D")(Call("B")(Call("A")(input_call)))
    output_call = Call("Z")(c, d)

    print("Original Graph:")
    output_call.print_graph()

    mod_output_call = op_commoning(output_call)

    print("\nModified Graph after op_commoning:")
    mod_output_call.print_graph()
