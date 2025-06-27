# ==== Abstract Graph Class ====
class Graph:
    def __init__(self):
        self.vertices = set()
        self.adjacency = {}  # Dictionary: vertex -> list of outgoing adjacent vertices

    def addVertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices.add(vertex)
            self.adjacency[vertex] = []

    def addEdge(self, from_vertex, to_vertex):
        if from_vertex in self.vertices and to_vertex in self.vertices:
            if to_vertex not in self.adjacency[from_vertex]:  # Avoid duplicates
                self.adjacency[from_vertex].append(to_vertex)

    def removeEdge(self, from_vertex, to_vertex):
        if from_vertex in self.adjacency and to_vertex in self.adjacency[from_vertex]:
            self.adjacency[from_vertex].remove(to_vertex)

    def listOutgoingAdjacentVertex(self, vertex):
        return self.adjacency.get(vertex, [])

    def listIncomingAdjacentVertex(self, vertex):
        return [v for v in self.vertices if vertex in self.adjacency.get(v, [])]

# ==== Person Entity Class ====
class Person:
    def __init__(self, user_id, name, gender, bio, is_public=True):
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.bio = bio
        self.is_public = is_public

    def get_profile(self, ignore_privacy=False):
        if self.is_public or ignore_privacy:
            return f"Name: {self.name}\nGender: {self.gender}\nBio: {self.bio}"
        else:
            return f"Name: {self.name}\n[This profile is private]"

# ==== Data Initialization ====
def setup_sample_data():
    people = {}

    p1 = Person("u1", "Sindy", "Female", "Loves cats and coffee", True)
    p2 = Person("u2", "Kai Shuang", "Female", "Software developer", True)
    p3 = Person("u3", "Brian", "Male", "Traveler and foodie", False)
    p4 = Person("u4", "Ke Ying", "Female", "Tech entrepreneur", False)
    p5 = Person("u5", "Sze Ying", "Female", "Gamer and YouTuber", True)

    for p in [p1, p2, p3, p4, p5]:
        people[p.user_id] = p

    graph = Graph()
    for user_id in people:
        graph.addVertex(user_id)

    graph.addEdge("u1", "u2")
    graph.addEdge("u5", "u2")
    graph.addEdge("u3", "u1")
    graph.addEdge("u4", "u1")

    return people, graph

# ==== CLI Menu ====
def run_social_media_app():
    people, graph = setup_sample_data()

    def find_user_id_by_name(name):
        for uid, person in people.items():
            if person.name.lower() == name.lower():
                return uid
        return None

    while True:
        print("\n****************************************")
        print("Welcome to Instagram, Your New Social Media App:")
        print("****************************************")
        print("1. View names of all profiles")
        print("2. View details for any profile (respects privacy)")
        print("3. View followers of any profile")
        print("4. View followed accounts of any profile")
        print("5. Add a new user profile")
        print("6. Follow another user")
        print("7. Unfollow a user")
        print("8. Quit")
        print("****************************************")
        choice = input("Enter your choice (1 - 8): ")

        if choice == "1":
            print("\n=== All Profile Names ===")
            for person in people.values():
                print(f"- {person.name}")

        elif choice == "2":
            name = input("Enter the name of the user to view their profile: ")
            uid = find_user_id_by_name(name)
            if uid:
                print("\n=== Profile Details ===")
                print(people[uid].get_profile(ignore_privacy=False))
            else:
                print("User not found.")

        elif choice == "3":
            name = input("Enter the name of the user to view their followers: ")
            uid = find_user_id_by_name(name)
            if uid:
                followers = graph.listIncomingAdjacentVertex(uid)
                print(f"\nFollowers of {people[uid].name}:")
                if followers:
                    for f in followers:
                        print(f"- {people[f].name}")
                else:
                    print("No followers.")
            else:
                print("User not found.")

        elif choice == "4":
            name = input("Enter the name of the user to view who they follow: ")
            uid = find_user_id_by_name(name)
            if uid:
                following = graph.listOutgoingAdjacentVertex(uid)
                print(f"\n{people[uid].name} is following:")
                if following:
                    for f in following:
                        print(f"- {people[f].name}")
                else:
                    print("Not following anyone.")
            else:
                print("User not found.")

        elif choice == "5":
            name = input("Enter name: ")
            if find_user_id_by_name(name):
                print("A user with this name already exists.")
                continue
            gender = input("Enter gender: ")
            bio = input("Enter biography: ")
            privacy = input("Is the profile public? (yes/no): ").lower()
            is_public = True if privacy == "yes" else False

            new_id = "u" + str(len(people) + 1)
            new_person = Person(new_id, name, gender, bio, is_public)
            people[new_id] = new_person
            graph.addVertex(new_id)
            print(f"User {name} has been added.")

        elif choice == "6":
            follower_name = input("Enter your name: ")
            followee_name = input("Enter the name of the user you want to follow: ")
            follower_id = find_user_id_by_name(follower_name)
            followee_id = find_user_id_by_name(followee_name)
            if follower_id and followee_id:
                if followee_id in graph.listOutgoingAdjacentVertex(follower_id):
                    print(f"Error: {follower_name} has already followed {followee_name}.")
                else:
                    graph.addEdge(follower_id, followee_id)
                    print(f"{follower_name} now follows {followee_name}.")
            else:
                print("One or both users not found.")

        elif choice == "7":
            follower_name = input("Enter your name: ")
            followee_name = input("Enter the name of the user you want to unfollow: ")
            follower_id = find_user_id_by_name(follower_name)
            followee_id = find_user_id_by_name(followee_name)
            if follower_id and followee_id:
                if followee_id in graph.listOutgoingAdjacentVertex(follower_id):
                    graph.removeEdge(follower_id, followee_id)
                    print(f"{follower_name} has unfollowed {followee_name}.")
                else:
                    print(f"Error: {follower_name} is not following {followee_name}.")
            else:
                print("One or both users not found.")

        elif choice == "8":
            print("Exiting Instagram. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

# ==== Run the App ====
run_social_media_app()
