import math
import turtle


class Plan():
    def __init__(self) -> None:
        pass


class Graph():
    def __init__(self) -> None:
        self.levels = 0
        self.act = {}
        self.act_mutexes = {}
        self.prop = {}
        self.prop_mutexes = {}


class Goal():
    def __init__(self) -> None:
        pass


class Planning():
    def __init__(self, input) -> None:
        self.__input = input

    def get_input(self, input: str) -> list:
        input_ls = self.__input.split('),')
        return self.fix_input(input_ls)

    def fix_input(self, input_ls):
        res = []

        for input in input_ls:
            input += ')'
            res.append(input)

        return res

    def get_dimensions(self, input_ls):
        greatest = 0

        for input in input_ls:
            if "Adj" in input:
                aa = input.split(',')
                a1 = int(aa[0].split('(')[1].replace('t', ''))
                a2 = int(aa[1].split(')')[0].replace('t', ''))

                gt = a1 if a1 > a2 else a1
                greatest = greatest if greatest > gt else gt

        # print("gratest: " + str(greatest))
        val = int(math.sqrt(greatest + 1))
        return (val, val)

    def get_flaws(self, goal, dimensions, input_ls):
        _, width = dimensions
        flaws = []
        position = goal[1]

        for input in input_ls:
            key = f'Adj({position}'
            if key in input:
                flaws.append({
                    'precondition': input,
                    'effect': goal
                })

        return flaws

    def get_start(self, input_ls: list) -> list:
        start = []

        for input in input_ls:
            if 'At' in input:
                start.append(input)
                break
        return start

    def build_link(self, input: str):
        a1 = input.split('(')
        a2 = a1[1].split(')')
        link = ('At', a2[0], a1[0])

        print("link " + str(link))

        return link

    def get_goals(self, input_ls: list) -> list:
        goals = []

        for input in input_ls:
            if 'Red' in input or 'Blue' in input:
                goals.append(self.build_link(input))

        return goals

    def get_steps(self, gvalues):
        steps = []
        for gvalue in gvalues:
            pass
        print("steps: " + str(steps))
        return steps

    def backtrack(self, plan, level):
        if level == 0:
            return plan
        new_g = []
        satisfied = True

        for goal in plan['g']:
            steps = self.get_steps(goal)

            plan['plan'] += steps
            new_g += self.get_preconditions(steps)

        self.backtrack(plan, level-1)

    def extract(self, graph: Graph, goal: set, index: int):
        if index == 0:
            return Plan()

        return self.search(graph, goal, Plan(), index)

    def search(self, graph: Graph, goal: set, plan: Plan, index: int):
        pass

    def plan(self, graph: Graph, goal: set):
        index = graph.levels - 1
        plan = self.extract(graph, goal, index)
        if plan:
            return plan
        while True:
            index += 1
            plan = self.extract(graph, goal, index)

            if plan:
                return plan

    def run(self) -> str:
        input_ls = self.get_input(input)
        dimensions = self.get_dimensions(input_ls)
        goals = self.get_goals(input_ls)
        starts = self.get_start(input_ls)

        # print("goals+ " + str(goals))
        # print("starts: " + str(starts))

        return input_ls[0]


while True:
    goal = input()
    print(Planning(goal).run())


# Command is current location folowed by target location
# Can only paint adjcent squares that have no paint
# Need to find actions to reach goal state
# Create plan with: steps, bindings, orderings, and causal links
