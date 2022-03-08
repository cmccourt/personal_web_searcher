import pickle

import searchWord
import webcrawler
from data_objects import URLGraph, IndexGraph, PageRank


class DBNotAvailable(Exception):
    print("WOOF! There is no database available. Please restore or build it")


def build_poodle_db():
    url_graph = URLGraph(webcrawler.getUrlLinks())
    index_graph = None
    page_rank = None
    # If the seed URL given isn't valid then return to main menu
    if url_graph is not None:
        index_graph = IndexGraph(_url_graph=url_graph.data)
        page_rank = PageRank(_url_graph=url_graph.data)
        print("POODLE Database created")
    else:
        print("URL could not be found.")
    return index_graph, page_rank, url_graph


def restore_poodle_db(index_graph: IndexGraph, page_rank: PageRank, url_graph: URLGraph):
    # User can use previous POODLE database using load_graphs function
    index_graph.data = index_graph.load_data_from_file(index_graph.default_file_path)
    page_rank.data = page_rank.load_data_from_file(page_rank.default_file_path)
    url_graph.data = url_graph.load_data_from_file(url_graph.default_file_path)
    print("Session restored")
    return index_graph, page_rank, url_graph


def save_graphs(url_graph, index_graph, page_rank):
    """Function that saves the url graph, index graph and
       page ranks into separate text files"""
    with open(index_graph.default_file_path, "w") as index_file:
        pickle.dump(index_graph.data, index_file)
    with open(url_graph.default_file_path, "w") as urls_file:
        pickle.dump(url_graph.data, urls_file)
    with open(page_rank.default_file_path, "w") as page_rank_file:
        pickle.dump(page_rank.data, page_rank_file)


def display_graphs(url_graph=None, index_graph=None, page_rank=None):
    """Function that displays the url graph, index graph and page rankings"""
    print("\n POODLE INDEX ----- \n ")
    index_graph.display_data()
    print("\nPOODLE GRAPH ----- \n ")
    url_graph.display_data()
    print("\nPOODLE RANKS ----- \n ")
    page_rank.display_data()
    print("\n")


def display_help():
    print("-build \t Create the POODLE database")
    print("-dump \t Save the POODLE database")
    print("-restore \t Retrieve the POODLE database")
    print("-print \t Show the POODLE database")
    print("-help \t Show this help information")
    print("-exit \t Exit the POODLE search engine")


def search_words_with_user_input(user_input, index_graph, page_rank):
    # User must have enter word(s) to search for
    try:
        search_result = searchWord.search_input(user_input, index_graph, page_rank)
        if search_result:
            if "Overall" in search_result:
                # There has been a match with the multiple words given
                if len(search_result["Overall"]) == 1:
                    # Only one matching URL so we only need to print it
                    print(f"WOOF! {user_input} was found!")
                    print(f"{search_result['Overall']}")
                else:
                    # Need to organise the URLs based on their page ranking
                    order_urls = sorted(search_result["Overall"], key=lambda x: x[1], reverse=True)
                    print(f"WOOF! {user_input} was found!")
                    for url_rank in order_urls:
                        print(f"{url_rank[0]} : {url_rank[1]}")
            else:
                # Couldn't find a common URL for the word(s) given so display the individual words instead
                print(f"WOOF! {user_input} could not be found but here the individual words were found!")
                url_tuple = sorted(search_result.items(), reverse=True, key=lambda x: x[1])
                for url_rank in url_tuple:
                    print(f"{url_rank[0]}: ")
                    for url in url_rank[1]:
                        print(f"{url}")
        else:
            # User input couldn't be found
            print(f"WOOF! {user_input} could not be found")
    # The user has tried to search for words without the database.
    except UnboundLocalError:
        raise DBNotAvailable


def main():
    """Main function that takes the user's input in the while loop
       and performs the function specified"""
    url_graph = URLGraph()
    index_graph = IndexGraph()
    page_rank = PageRank()
    is_exit = False
    while not is_exit:
        user_input = input("WOOF! What would you like to do? ->")
        if user_input == '-build':
            index_graph, page_rank, url_graph = build_poodle_db()
        elif user_input == '-dump':
            # If user tries to save the graphs before building or restoring them, POODLE will prompt them
            save_graphs(url_graph, index_graph, page_rank)
            print("Database saved")
        elif user_input == '-restore':
            index_graph, page_rank, url_graph = restore_poodle_db(index_graph, page_rank, url_graph)
        elif user_input == '-print':
            # If user tries to print the graphs before building or restoring them, POODLE will prompt them
            display_graphs(url_graph, index_graph, page_rank)
        elif user_input == '-help':
            # Displays help list
            display_help()
        elif user_input == '-exit':
            # Exits the application
            is_exit = True
        elif user_input[0] == '-':
            # The input given from user isn't valid
            print("WOOF! This is not a valid option. Use -help for list of functions")
        else:
            search_words_with_user_input(user_input, index_graph, page_rank)


if __name__ == "__main__":
    main()
