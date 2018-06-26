from __future__ import print_function
import cobra.test
from cobra import Model, Reaction, Metabolite

# "textbook" and "salmonella" are also valid arguments
model = cobra.test.create_test_model("ecoli")

# print(len(model.reactions))
# print(len(model.metabolites))
# print(len(model.genes))

reactions = {"HEX1", "PGI", "PFK", "FBA", "TPI", "GAPD", "PGK", "PGM", "ENO", "PYK"}

for r in reactions:
    print(r)

cobra_model = Model("Model_assignment9")

fo = open("Output.txt", "w+")


# Here we add the specific reactions we need in our new model
# add_reaction is deprecated but it doesn't seem to work with add_reactions and the documentation is hard to read
#cobra_model.add_reactions(model.reactions.get_by_id(reactions))

for r in reactions:
    cobra_model.add_reaction(model.reactions.get_by_id(r))

print("\n---------------------------------------\nReactions\n---------------------------------------")

fo.write("Reactions\n")

for reaction in cobra_model.reactions:
    s = "%s : %s" % (reaction.id, reaction.reaction)
    print(s)
    fo.writelines(s + "\n")

fo.write("\nMetabolites\n")
print("\n---------------------------------------\nMetabolites\n---------------------------------------")
for x in cobra_model.metabolites:
    s = '%s : %s' % (x.id, x.formula)
    print(s)
    fo.writelines(s + "\n")


fo.write("\nGenes\n")
print("\n---------------------------------------\nGenes\n---------------------------------------")

for gene in cobra_model.genes:
    reactions_list_str = "{" + ", ".join((i.id for i in gene.reactions)) + "}"
    print("%s is associated with reactions: %s" % (gene.id, reactions_list_str))
    fo.writelines("%s is associated with reactions: %s" % (gene.id, reactions_list_str) + "\n")

fo.close()

print("Number of reactions")
print(len(cobra_model.reactions))

print("Number of genes")
print(len(cobra_model.genes))

print("Number of metabolites")
print(len(cobra_model.metabolites))