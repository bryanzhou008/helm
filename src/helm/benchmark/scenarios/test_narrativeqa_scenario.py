import pytest
from tempfile import TemporaryDirectory

from helm.benchmark.scenarios.narrativeqa_scenario import NarrativeQAScenario
from helm.benchmark.scenarios.scenario import CORRECT_TAG, Output, Reference


@pytest.mark.scenarios
def test_narrativeqa_scenario():
    scenario = NarrativeQAScenario()
    with TemporaryDirectory() as tmpdir:
        instances = scenario.get_instances(tmpdir)
    assert len(instances) == 1572
    assert (
        instances[0].input.text
        == "At Madeline Hall, an old mansion-house near Southampton belonging to the wealthy de Versely family, lives"
        " an elderly spinster Miss Delmar, the aunt of the earl de Versely and Captain Delmar. Miss Delmar invites"
        " Arabella Mason, the daughter of a deceased, well-liked steward to stay with her as a lower-class guest in"
        " the house. Captain Delmar is known to visit his aunt at Madeline Hall frequently, accompanied by his"
        " valet Ben Keene, who is also a private marine. Captain Delmar eventually suggests that Ben should propose"
        " to Arabella, and the two marry in secret, to the frustration of Miss Delmar and Arabella's mother. The"
        " captain is able to smooth over the situation with his aunt, even after it is discovered that Arabella was"
        " six months pregnant at the time of the marriage. She later gives birth to a boy, who takes the Captain's"
        " Christian name and Ben's surname--the titular Percival Keene.\nThe family moves to Chatham, after Ben is"
        " ordered back with his detachment. Arabella opens up a successful shop and circulating library below her"
        " house, enlisting the help of her mother and sister, Amelia. Percival becomes well known in town from his"
        " mischievous pranks on officers and other strangers, often encouraged by his aunt Amelia. However,"
        " Percival's mother and grandmother are less fond of his disregard for manners, and insist on sending him"
        " to school after an episode in which he bites his grandmother. Percival reports to the school house of Mr."
        " O'Gallagher, a poor Irish scholar, who rules his class with a system of severe corporal punishment. Mr."
        " O'Gallagher routinely bullies Percival by stealing his lunch, leading Percival to seek revenge by"
        " poisoning his sandwiches with calomel. On Guy Fawkes Day the schoolteacher confiscates all the"
        " schoolboys' fireworks, for which Percival retaliates by setting off the collected fireworks while the"
        " teacher sits above them, leading to the total destruction of the schoolhouse and near death of the"
        " schoolmaster.\nWhen Percival is a young teenager, Captain Delmar reappears and offers him a position"
        " aboard his new navy ship, the H.M. Calliope. While preparing to enter service, Percival overhears gossip"
        " of his illegitimate birth, introducing the idea that Captain Delmar may be his father. He confronts his"
        " mother about his parentage, which she at first harshly denies but later tearfully explains the truth of"
        " her affair. Early in his service in the navy, Percival is captured during a pirate raid along with"
        " others. The pirate crew is entirely black, and the captain explains that they are primarily escaped"
        " slaves from the Americas. Percival is taken in as a cabin boy, and later dyes his skin tan in the"
        " appearance of a mulatto to please the captain who doesn't approve of white skin. The pirates often seek"
        " to take over slave trading vessels, killing every white person on board. During the taking of one such"
        " vessel, Percival is able is convince the captain to spare the lives of a wealthy Dutch merchant and his"
        " young daughter, Minnie. Eventually the H.M. Calliope takes the pirate ship, and Percival--unrecognizable"
        " with his dyed skin--is taken as a prisoner, later to convince his fellow shipman of his true"
        " identity.\nAfter his reappearance aboard the ship, Percival gains esteem among the crew and is welcomed"
        " back by the emotional Captain Delmar. His reputation continues to grow over the course of his service in"
        " conflicts with Dutch and French vessels around the island of Curacao. He also stands in for an ill"
        " Captain Delmar in a duel with a French officer, effectively saving the captain's life. At this point, the"
        " captain receives news that his older brother has died, making him the new Lord de Versely, and before"
        " returning to England he grants Perceval command of his own schooner. After another intense but successful"
        " battle with a French war ship, Percival is promoted to captain. During his service in the Navy, Percival"
        " still partakes in the merry pranks of his youth, and at one point teams up with a mulatto hotel owner in"
        " Curaรงao to convince his fellow officers they've been poisoned. He also keeps correspondence with Minnie,"
        " developing a romance with the beautiful heiress.\nNear the end of the story, Percival guides his crew"
        " through a terrible storm in which many of the crew are killed and the ship is heavily damaged. After"
        " being saved by another English vessel, he receives a letter informing him of Lord de Versely's sudden"
        " death from heart complications and learns that he has been left all of his personal property. Percival is"
        " still disappointed that he can not take his father's name. He later journey's with his friend Bob Cross"
        " to Hamburg to reunite with Minnie, but is captured by French troops on the road and sentenced to"
        " execution for spying. During a skirmish between the French and the Cossacks, Percival and Cross are able"
        " to escape and continue on the road. At the end of the novel, Percival proposes to Minnie, and stands to"
        " inherit a great fortune through her father. He also receives a letter from the de Versely attorney"
        " letting him know he has been granted the arms and name of Delmar.\nQuestion: Who did Percival reunited"
        " with?"
    )

    assert instances[0].references == [
        Reference(output=Output(text="Minnie"), tags=[CORRECT_TAG]),
        Reference(output=Output(text="minnie"), tags=[CORRECT_TAG]),
    ]
    assert instances[0].split == "train"
