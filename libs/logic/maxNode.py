import backend.node as node

class maxNode(node.Node):
    name = "Max node"
    description = "This is a node designed to find the maximum of two numbers."
    color = [0.3, 0.6, 0.9, 1]
    CInformationBase = """
    long long Max(long long A, long long B) {
        return A > B ? A : B;
    }
    """

    def __init__(self) -> None:
        super().__init__(["Work", "A", "B"], ["Result"], ["Base", "Add"])
        
    def eval(self) -> None:
        if self.inputs["Work"] == None or self.inputs["Work"].eval() <= 0:
            self.outputs["Result"] = None
        else:
            self.outputs["Result"] = node.ValueType().setParam("Value", self.inputs['A'].eval() or self.inputs['B'].eval())
    
    def code(self) -> str:
        if self.inputs["Work"] == None:
            return "0"
        elif self.inputs["Work"].eval() <= 0:
            return "0"
        return f"Max({self.inputs['A'].code()}, {self.inputs['B'].code()})"