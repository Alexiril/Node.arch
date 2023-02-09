import backend.node as node

class minNode(node.Node):
    name = "Min node"
    description = "This is a node designed to find the minimum of two numbers."
    color = [0.3, 0.6, 0.9, 1]
    CInformationBase = """
    long long Min(long long A, long long B) {
        return A < B ? A : B;
    }
    """

    def __init__(self) -> None:
        super().__init__(["Work", "A", "B"], ["Result"], ["Base"])
        
    def eval(self) -> None:
        if self.inputs["Work"] == None or self.inputs["Work"].eval() <= 0:
            self.outputs["Result"] = None
        else:
            self.outputs["Result"] = node.ValueType().setParam("Value", self.inputs['A'].eval() and self.inputs['B'].eval())
    
    def code(self) -> str:
        if self.inputs["Work"] == None:
            return "0"
        elif self.inputs["Work"].eval() <= 0:
            return "0"
        return f"Min({self.inputs['A'].code()}, {self.inputs['B'].code()})"