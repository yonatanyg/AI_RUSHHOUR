from action_layer import ActionLayer
from util_pmodel import Pair
from proposition import Proposition
from proposition_layer import PropositionLayer


class PlanGraphLevel(object):
    """
    A class for representing a level in the plan graph.
    For each level i, the PlanGraphLevel consists of the actionLayer and propositionLayer at this level in this order!
    """
    independent_actions = set()  # updated to the independent_actions of the problem (graph_plan.py line 32)
    actions = []  # updated to the actions of the problem (graph_plan.py line 33 and planning_problem.py line 36)
    props = []  # updated to the propositions of the problem (graph_plan.py line 34 and planning_problem.py line 36)

    @staticmethod
    def set_independent_actions(independent_actions):
        PlanGraphLevel.independent_actions = independent_actions

    @staticmethod
    def set_actions(actions):
        PlanGraphLevel.actions = actions

    @staticmethod
    def set_props(props):
        PlanGraphLevel.props = props

    def _init_(self):
        """
        Constructor
        """
        self.action_layer = ActionLayer()  # see action_layer.py
        self.proposition_layer = PropositionLayer()  # see proposition_layer.py

    def get_proposition_layer(self):  # returns the proposition layer
        return self.proposition_layer

    def set_proposition_layer(self, prop_layer):  # sets the proposition layer
        self.proposition_layer = prop_layer

    def get_action_layer(self):  # returns the action layer
        return self.action_layer

    def set_action_layer(self, action_layer):  # sets the action layer
        self.action_layer = action_layer

    def update_action_layer(self, previous_proposition_layer):
        """
        Updates the action layer given the previous proposition layer (see proposition_layer.py)
        You should add an action to the layer if its preconditions are in the previous propositions layer,
        and the preconditions are not pairwise mutex.
        all_actions is the set of all the action (include noOp) in the domain
        You might want to use those functions:
        previous_proposition_layer.is_mutex(prop1, prop2) returns true
        if prop1 and prop2 are mutex at the previous propositions layer
        previous_proposition_layer.all_preconds_in_layer(action) returns true
        if all the preconditions of action are in the previous propositions layer
        self.actionLayer.addAction(action) adds action to the current action layer
        """
        all_actions = PlanGraphLevel.actions

        def check_action(action, previous_proposition_layer):
            if not previous_proposition_layer.all_preconds_in_layer(action):
                return False

            preconds = action.get_pre()
            for p1 in preconds:
                for p2 in preconds:
                    if not (p1 == p2):
                        if previous_proposition_layer.is_mutex(p1, p2):
                            return False
            return True

        for action in all_actions:
            if check_action(action, previous_proposition_layer):
                self.action_layer.add_action(action)

    def update_mutex_actions(self, previous_layer_mutex_proposition):
        """
        Updates the mutex set in self.action_layer,
        given the mutex proposition from the previous layer.
        current_layer_actions are the actions in the current action layer
        You might want to use this function:
        self.actionLayer.add_mutex_actions(action1, action2)
        adds the pair (action1, action2) to the mutex set in the current action layer
        Note that an action is not mutex with itself
        """
        current_layer_actions = list(self.action_layer.get_actions())
        "* YOUR CODE HERE *"
        for i in range(len(current_layer_actions)):
            for j in range(i + 1, len(current_layer_actions)):
                action1 = current_layer_actions[i]
                action2 = current_layer_actions[j]
                if mutex_actions(action1, action2, previous_layer_mutex_proposition):
                    self.action_layer.add_mutex_actions(action1, action2)


    def update_proposition_layer(self):
        """
        Updates the propositions in the current proposition layer,
        given the current action layer.
        don't forget to update the producers list!
        Note that same proposition in different layers might have different producers lists,
        hence you should create two different instances.
        current_layer_actions is the set of all the actions in the current layer.
        You might want to use those functions:
        dict() creates a new dictionary that might help to keep track on the propositions that you've
               already added to the layer
        self.proposition_layer.add_proposition(prop) adds the proposition prop to the current layer

        """

        def add_to_dict(my_dict, action, prop_name):
            if prop_name in my_dict:
                my_dict[prop_name].add(action)
            else:
                my_dict[prop_name] = {action}

        current_layer_actions = self.action_layer.get_actions()
        prop_actions_dic = {}

        for action in current_layer_actions:
            if action.is_noop():
                prev_prop = action.get_pre()[0]
                add_to_dict(prop_actions_dic, action, prev_prop.get_name())
            else:
                new_props = action.get_add()
                for prop in new_props:
                    add_to_dict(prop_actions_dic, action, prop.get_name())

        for prop_name, producers in prop_actions_dic.items():
            prop = Proposition(prop_name)
            prop.set_producers(list(producers))
            self.proposition_layer.add_proposition(prop)




    def update_mutex_proposition(self):
        """
        updates the mutex propositions in the current proposition layer
        You might want to use those functions:
        mutex_propositions(prop1, prop2, current_layer_mutex_actions) returns true
        if prop1 and prop2 are mutex in the current layer
        self.proposition_layer.add_mutex_prop(prop1, prop2) adds the pair (prop1, prop2)
        to the mutex set of the current layer
        """
        current_layer_propositions = list(self.proposition_layer.get_propositions())
        current_layer_mutex_actions = self.action_layer.get_mutex_actions()

        for i in range(len(current_layer_propositions)):
            for j in range(i + 1, len(current_layer_propositions)):
                prop1 = current_layer_propositions[i]
                prop2 = current_layer_propositions[j]

                if mutex_propositions(prop1, prop2, current_layer_mutex_actions):
                    self.proposition_layer.add_mutex_prop(prop1, prop2)

    def expand(self, previous_layer):
        """
        Your algorithm should work as follows:
        First, given the propositions and the list of mutex propositions from the previous layer,
        set the actions in the action layer.
        Then, set the mutex action in the action layer.
        Finally, given all the actions in the current layer,
        set the propositions and their mutex relations in the proposition layer.
        """
        # Retrieve mutex propositions from the previous proposition layer
        previous_proposition_layer = previous_layer.get_proposition_layer()
        previous_layer_mutex_proposition = previous_proposition_layer.get_mutex_props()

        # Initialize the action layer and update actions based on previous propositions
        self.set_action_layer(ActionLayer())
        self.update_action_layer(previous_proposition_layer)

        # Update mutex actions based on mutex propositions from previous layer
        self.update_mutex_actions(previous_layer_mutex_proposition)

        # Initialize the proposition layer and update propositions and their mutex relations
        self.set_proposition_layer(PropositionLayer())
        self.update_proposition_layer()
        self.update_mutex_proposition()

    def expand_without_mutex(self, previous_layer):
        """
        Questions 11 and 12
        You don't have to use this function
        """
        previous_layer_proposition = previous_layer.get_proposition_layer()
        "* YOUR CODE HERE *"
        self.set_action_layer(ActionLayer())
        self.update_action_layer(previous_layer_proposition)

        self.set_proposition_layer(PropositionLayer())
        self.update_proposition_layer()


def mutex_actions(a1, a2, mutex_props):
    """
    This function returns true if a1 and a2 are mutex actions.
    We first check whether a1 and a2 are in PlanGraphLevel.independent_actions,
    this is the list of all the independent pair of actions (according to your implementation in question 1).
    If not, we check whether a1 and a2 have competing needs
    """
    if Pair(a1, a2) not in PlanGraphLevel.independent_actions:
        return True
    return have_competing_needs(a1, a2, mutex_props)


def have_competing_needs(a1, a2, mutex_props):
    """
    Determine whether actions a1 and a2 have competing needs,
    given the mutex propositions from the previous level.

    Arguments:
    a1 -- The first action.
    a2 -- The second action.
    mutex_props -- A list of pairs of propositions that are mutex.

    Returns:
    bool -- True if a1 and a2 have competing needs, False otherwise.
    """
    for p in a1.get_pre():
        for q in a2.get_pre():
            if not (p == q) and Pair(p, q) in mutex_props:
                return True

    return False


def mutex_propositions(prop1, prop2, mutex_actions_list):
    """
    complete code for deciding whether two propositions are mutex,
    given the mutex action from the current level (set of pairs of actions).
    Your update_mutex_proposition function should call this function
    You might want to use this function:
    prop1.get_producers() returns the set of all the possible actions in the layer that have prop1 on their add list
    """
    "* YOUR CODE HERE *"
    # Get the sets of actions that produce prop1 and prop2
    prod1 = prop1.get_producers()
    prod2 = prop2.get_producers()

    # Check if all combinations of producers are mutex
    for a in prod1:
        for b in prod2:
            if not (a == b) and Pair(a, b) not in mutex_actions_list:
                return False  # Found a non-mutex pair, so the propositions are not mutex

    # If all pairs are mutex, return True
    return True