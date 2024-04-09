import BitVector


class KnapsackSolution:

    def __init__(self, vector: BitVector.BitVector, weight: int, value: int, valid: bool):
        self.vector = vector
        self.weight = weight
        self.value = value
        self.valid = valid
        self.info = {}

    def __eq__(self, other):
        return self.vector == other.vector

    @property
    def selected(self):
        return self.vector.count_bits()


class KnapsackProblem:

    def __init__(self):
        self._id = 0
        self._weights: list[int] = []
        self._values: list[int] = []
        self._ratios: list[float] = []
        self._ratio_indices: list[int] = []
        self.weight_limit = 0
        self.value_limit = 0

    def update_ratios(self):
        self._ratios = []
        for i in range(len(self._weights)):
            self._ratios.append(self._values[i] / self._weights[i])
        self._ratio_indices = sorted(range(len(self._ratios)), key=lambda i: self._ratios[i], reverse=True)

    @property
    def size(self):
        return len(self._weights)

    def __getitem__(self, item):
        return self._values[item], self._weights[item]

    def repair(self, solution: KnapsackSolution) -> KnapsackSolution:
        if solution.weight <= self.weight_limit:
            return solution
        # Unselect items with the lowest value/weight ratio
        # (alternatively could try random repair, or other heuristics)
        vector = solution.vector.deep_copy()
        weight = solution.weight
        for i in self._ratio_indices:
            if vector[i]:
                vector[i] = False
                weight -= self._weights[i]
                if weight <= self.weight_limit:
                    break
        return self.evaluate(vector)

    def evaluate(self, vector: BitVector.BitVector) -> KnapsackSolution | None:
        total_value = 0
        total_weight = 0
        for i in range(len(self._weights)):
            if vector[i]:
                total_value += self._values[i]
                total_weight += self._weights[i]
        if total_weight > self.weight_limit:
            total_value = 0
        return KnapsackSolution(
            vector=vector,
            weight=total_weight,
            value=total_value,
            valid=total_weight <= self.weight_limit,
        )

    def load_json(self, json_data: dict):
        self._weights.clear()
        self._values.clear()
        for item in json_data.get('items'):
            self._weights.append(item['weight'])
            self._values.append(item['value'])
        self.weight_limit = json_data['weight_limit']
        self.update_ratios()

    def load_line(self, input_line: str):
        self._weights.clear()
        self._values.clear()
        parts = input_line.strip().split()
        self._id = int(parts[0])
        n = int(parts[1])
        self.weight_limit = int(parts[2])
        index = 3
        if self._id < 0:
            self.value_limit = int(parts[index])
            index += 1
        end = 2 * n + index
        while index < end:
            self._weights.append(int(parts[index]))
            self._values.append(int(parts[index+1]))
            index += 2
        self.update_ratios()

    def result_line(self, solution: KnapsackSolution) -> str:
        bits = str(solution.vector).replace("", " ")[1:-1]
        return f'{self._id} {len(self._weights)} {solution.value} {bits}'
