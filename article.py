##################################################################
# FILE : article.py
# WRITER : Yulia Feldman
# DESCRIPTION: article.py contains the class Article which represents an article.
##################################################################
import copy


class Article:
    """
    This class represents an article.
    """
    def __init__(self, article_title):
        """
         A constructor for the object article.
        :param article_title: the title of the article.
        """
        self.__article_title = article_title
        self.__neighbors = list()

    def get_title(self):
        """
        :return: The title of the article
        """
        return self.__article_title

    def add_neighbor(self, neighbor):
        """
        :param neighbor: An Article object
        :return: adds neighbor to the list of this article neighbors
               """
        if neighbor not in self.__neighbors:
            self.__neighbors.append(neighbor)

    def get_neighbors(self):
        """
        :return: a list of articles that this article refers to.
        """
        return copy.copy(self.__neighbors)

    def __len__(self):
        """
        :return: returns the number of this article's neighbors
        """
        return len(self.__neighbors)

    def __repr__(self):
        """
        :return: A string representation of this article in the following
        format: a tuple which contains the name of this article and A list
        of all the article's neighbors.
        """

        str = '(\'' + self.__article_title + '\', ['

        for i in range(self.__len__()):
            str += '\''
            str += self.__neighbors[i].__article_title
            str += '\''
            if i < self.__len__() - 1:
                str += ', '
        str += '])'

        return str

    def __contains__(self, article):
        """
        :param article: An Article object
        :return: True if the received article is in this article's neighbors
        list. False, otherwise.
        """
        return article in self.__neighbors
