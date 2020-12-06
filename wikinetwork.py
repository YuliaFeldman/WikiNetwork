##################################################################
# FILE : article.py
# WRITER : Yulia Feldman 
# DESCRIPTION: wikinetwork.py contains contains the class
# WikiNetwork which represents a network of objects of the class Article.
##################################################################

from article import Article
import copy

DEFAULT_DIVISOR = 0.9
INITIAL_RANK = 1

def read_article_links(filename):
    """
    Function receives a name of a file and returns a list of tuples- each
    tuple contains names of two articles.
    """
    couples_of_articles = list()
    file_txt = open(filename, 'r')
    line = file_txt.readline()

    while line is not '':
        temp = line.split('\t')
        article_A = temp[0]
        article_B = temp[1]
        temp = article_B.split('\n')
        article_B = temp[0]
        couples_of_articles.append((article_A, article_B))
        line = file_txt.readline()

    file_txt.close()
    return couples_of_articles

##############################################################################


class WikiNetwork:
    """
    This class represents a network of object of the type article.
    """
    def __init__(self, link_list):
        """
        :param link_list: a list of tuples. Each tuple contains a name of an
        article and the name of the referred article.
        """
        self.__collection = dict()
        self.update_network(link_list)

    def update_network(self, link_list):
        """
        :param link_list: a list of tuples. Each tuple contains a name of an
        article and the name of the referred article.
        Method updates this wikinetwork with the new details from link_list
        """
        for couple in link_list:
            if couple[0] not in self.__collection.keys() \
                    and couple[1] not in self.__collection.keys():

                article_A = Article(couple[0])
                article_B = Article(couple[1])
                article_A.add_neighbor(article_B)

                self.__collection[couple[0]] = article_A
                self.__collection[couple[1]] = article_B

            elif couple[0] in self.__collection.keys() \
                    and couple[1] not in self.__collection.keys():

                article = Article(couple[1])
                self.__collection[couple[0]].add_neighbor(article)
                self.__collection[couple[1]] = article

            elif couple[0] in self.__collection.keys() \
                    and couple[1] in self.__collection.keys():

                self.__collection[couple[0]].add_neighbor(
                    self.__collection[couple[1]])

            else:
                article = Article(couple[0])
                article.add_neighbor(self.__collection[couple[1]])
                self.__collection[couple[0]] = article

    def get_articles(self):
        """
        :return: A list of all the articles in this wikinetwork.
        """
        lst = list()
        for article in self.__collection.values():
            lst.append(article)
        return copy.copy(lst)

    def get_titles(self):
        """
        :return: A list of all the article's titles in this wikinetwork.
        """
        lst = list()
        for title in self.__collection.keys():
            lst.append(title)
        return copy.copy(lst)

    def __contains__(self, title):
        """
        :param title: a string that represents a title of an article
        :return: True if the article, that it's title is the received title,
        is in this wikinetwork, False otherwise.
        """
        return title in self.get_titles()

    def __len__(self):
        """
        :return: The number of articles in this wikinetwork.
        """
        return len(self.__collection)

    def __repr__(self):
        """
        :return: A string representation of this wikinetwork.
        """
        return str(self.__collection)

    def __getitem__(self, title):
        """
        :param title: A string that represents a name of an article.
        :return: The article that it's title is the received title.
        """
        if title in self.__collection.keys():
            return self.__collection[title]
        else:
            raise KeyError(title)

    def page_rank(self, iters, d=DEFAULT_DIVISOR):
        """
        :param iters: An integer number
        :param d: A number that represents a divisor in the algorithm
        :return: A list of titles of the articles ranked by they're
        "page rank", from highest to lowest.
        If two articles have the same "page rank", they will be placed in the
        returned list in an alphabet order.
        """

        ranks = dict()  # will save the rank of each article

        articles = self.get_articles()
        titles = self.get_titles()

        # setting the rank of each article to be 1
        ranks = self.__set_ranks__(ranks, titles, INITIAL_RANK)

        for i in range(iters):
            ranks_in_iter = copy.copy(ranks)
            ranks = self.__set_ranks__(ranks, titles, INITIAL_RANK-d)
            for article in articles:

                title = article.get_title()
                num_of_neighbors = article.__len__()

                if num_of_neighbors == 0:
                    rank_for_all = d * ranks_in_iter[title] / self.__len__()

                    ranks = self.__update_ranks__(ranks, titles,
                                                  rank_for_all)

                else:
                    rank_for_neighbor = d * ranks_in_iter[title] / \
                                        num_of_neighbors
                    neighbors_of_article = article.get_neighbors()

                    titles_of_neighbors = list()
                    for n in neighbors_of_article:
                        titles_of_neighbors.append(n.get_title())

                    ranks = self.__update_ranks__(ranks, titles_of_neighbors,
                                                  rank_for_neighbor)

        temp = self.__sort__(ranks)
        returned_list = list()
        for item in temp:
            returned_list.append(item[0])
        return returned_list

    def __sort__(self, ranks):
        """

        :param ranks: A dictionary type object which contains ranks of
        articles
        :return: A sorted list of tuples, from highest to lowest. Each tuple
        contains article's name and it's rank.
        """
        lst = list()
        for rank in ranks:
            lst.append((rank, ranks[rank]))

        sorted_lst = sorted(lst, key=lambda tup: tup[1], reverse=True)

        i = 0
        while i < self.__len__()-1:
            if sorted_lst[i][1] == sorted_lst[i+1][1]:
                index = i
                temp_lst = list()
                temp_lst.append(sorted_lst[i])
                temp_lst.append(sorted_lst[i+1])
                j = i+2
                while j < self.__len__()\
                        and sorted_lst[i][1] == sorted_lst[j][1]:
                    temp_lst.append(sorted_lst[j])
                    j += 1
                i = j-1
                temp_lst = sorted(temp_lst, key=lambda tup: tup[0])

                k = 0
                while index < i+1:
                    sorted_lst[index] = temp_lst[k]
                    index +=1
                    k += 1
            i += 1

        return sorted_lst

    def __set_ranks__(self, ranks, titles, points):
        for title in titles:
            ranks[title] = points
        return ranks

    def __update_ranks__(self, ranks, titles, points):
        for title in titles:
            ranks[title] += points
        return ranks

    def jaccard_index(self, article_title):
        """
        :param article_title: a string representation of a title of an
        article.
        :return: A list of articles names ranked by they're "Jaccard
        index", from highest to lowest.
        """
        if not self.__contains__(article_title) \
                or not self.__collection[article_title].get_neighbors():
            return None
        else:
            article_A = self.__collection[article_title]
            neighbors_A = set(article_A.get_neighbors())
            temp_dict = dict()

            for article_B in self.__collection:
                neighbors_B = \
                    set(self.__collection[article_B].get_neighbors())
                intersection = neighbors_A.intersection(neighbors_B)
                if intersection == set():
                    intersection = 0
                else:
                    intersection = intersection.__len__()

                union = neighbors_A.union(neighbors_B)
                union = union.__len__()
                jaccard_index = intersection/union
                temp_dict[article_B] = jaccard_index
            temp = self.__sort__(temp_dict)
            returned_list = list()
            for item in temp:
                returned_list.append(item[0])
            return returned_list

    def __entrance_level__(self, article):
        """

        :param article: An article type object
        :return: the number of article's incoming neighbors
        """
        level = 0
        for item in self.__collection:
            neighbors = self.__collection[item].get_neighbors()
            if article in neighbors:
                level += 1
        return level

    def __get_path__(self, article_A, article_B):
        """

        :param article_A: An article type object
        :param article_B: An article type object
        :return: The more suitable article to be the next step in path
        """
        level_A = self.__entrance_level__(article_A)
        level_B = self.__entrance_level__(article_B)

        if level_A > level_B:
            return article_A
        elif level_B > level_A:
            return article_B
        else:
            if article_A.get_title() < article_B.get_title():
                return article_A
            else:
                return article_B

    def travel_path_iterator(self, article_title):
        """
        :param article_title: a string that represents a title of an article.
        :return: An iterator that returns articles' names in a
        path, according to their order.
        """
        if article_title not in self:
            raise StopIteration

        while self.__collection[article_title].__len__() > 0:
            yield article_title
            article = self.__collection[article_title]

            # sorted list of neighbors according to their entrance level
            sorted_neighbors = sorted(article.get_neighbors(), key=lambda x:
                ((-1) * self.__entrance_level__(x), x.get_title()))

            article_title = sorted_neighbors[0].get_title()
            self.travel_path_iterator(article_title)

        # last article in path (the article which has no neighbors)
        yield article_title
        raise StopIteration

    def friends_by_depth(self, article_title, depth):
        """
        :param article_title: a string that represents a name of an article.
        :param depth: an integer that represents a level of "closeness"
        :return: a list of all the titles of the articles that are "close" to
        the received article with the same level as the depth received.
        """
        if article_title not in self:
            return None
        friends = set()

        def find_friends_by_depth(title, depth, count_steps, friends):

            if count_steps < depth and len(self.__collection[title]) > 0:

                article = self.__collection[title]
                sorted_neighbors = sorted(article.get_neighbors(),
                key=lambda x: ((-1) * self.__entrance_level__(x),
                               x.get_title()))

                next_titles = list()
                for neighbor in sorted_neighbors:
                    next_titles.append(neighbor.get_title())
                next_titles.append(title)

                for t in next_titles:
                    friends = find_friends_by_depth(
                        t, depth, count_steps + 1, friends)

            friends.add(title)
            return friends

        return list(find_friends_by_depth(article_title, depth, 0, friends))
