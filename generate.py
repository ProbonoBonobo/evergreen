import random

def Grammar(**grammar):
    "Create a dictionary mapping symbols to alternatives."
    for (cat, rhs) in grammar.items():
        grammar[cat] = [alt.split() for alt in rhs.split('|')]
    return grammar

grammar = Grammar(
    STEMS='IMP PREP_PHRASE | FP_VERB FP_TYPE FP_CONCEPT FP_PREP FP_TYPE FP_CONCEPT | IMP DAT_PP FP_TYPE FP_CONCEPT |  IMP ADJ FP_TYPE FP_CONCEPT | IMP ACC_PP FP_TYPE FP_CONCEPT | FP_VERB FP_ADJ FP_TYPE FP_CONCEPT FP_PREP FP_TYPE FP_CONCEPT | FP_VERB FP_RELATION FP_TYPE FP_CONCEPT ',
    MATH_VERBS='show | prove that the',
    FP_VERB = 'convert | reduce | transform',
    PREP_PHRASE = 'ADJ ACC_PP DO | ADJ DAT_PP DO | ACC_PP DO | DAT_PP DO',
    IMP='save | merge | add | resolve | override | remove | export | fix ',
    FP_ADJ = 'curried | forgetful | surjective | bijective | self-adjoint | free | natural | representable | partial | pure | composible | non-blocking | endomorphic | applicative | recursive | immutable | recurrent | idempotent | traversible | foldable | point-free | lazy | referential | pointed | symmetric | stateless',
    ADJ="broken | orphaned  | parent | asynchronous | local | default | working | redundant | hyper| every | temp | some ",
    FP_TYPE =  'state | identity | Kolmogorov | Yoneda | Kleisli | universal | point-free | Weil | non-abundant | coherent | Einstein-Rieman-Roch | Dirac | nonabelian | derived | algebraic | Boltzmann | anabelian | Galois | von Neumann | differential | Chaitin | Riemann | tensor | geometric | imaginary | continuation | IO | sequence | finite-state',
    FP_CONCEPT = 'functor | extensions | embedding | twistor | interpretation | conjecture | K-theory | apparatus | manifold | complexity | continuation | sheaves | transducer | complexity | union | reducer | categories | comonad | monoid | morphism | bundle | scheme | sequence | semigroup | setoid | calculi',
    FP_RELATION = 'instance of | subcategory of | proof of | extension of | unit of ',
    FP_PREP = 'into',
    PREP = 'from',
    ACC_PP = 'path to | link to | reference to ',
    DAT_PP = "path from | link from | reference from | variable from | environment from | invocation of | status from | state of ",
    DO="$PYTHONPATH | build script | coroutine | threadpool | posix api | subprocess | shell | API | cron | install.sh | shell | cache | requirements.txt | package.json | event-loop | .evergreen_data | python environment | venv | VM | github | package manager | apt-get | homebrew "
)


def make_issue(symbol='STEMS'):
    "Replace symbol with a random entry in grammar (recursively); join into a string."
    if symbol not in grammar:
        return symbol
    else:
        words = map(make_issue, random.choice(grammar[symbol]))
        phrase = ' '.join(words).capitalize()
        return phrase


def punctuate(phrase):
    return "".join([phrase, ". "])
