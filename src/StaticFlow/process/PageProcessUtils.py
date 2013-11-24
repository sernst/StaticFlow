# PageProcessUtils.py
# (C)2013
# Scott Ernst

#___________________________________________________________________________________________________ PageProcessUtils
class PageProcessUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ sortPagesByDate
    @classmethod
    def sortPagesByDate(cls, pages, reverse =False):
        """ Sorts the list of Page in order of their date from oldest to newest unless reversed """

        if not pages or len(pages) < 2:
            return pages

        out = [pages[0]]
        src = pages[1:]
        while len(src) > 0:
            page = src.pop()
            for i in range(len(out)):
                if page.date > out[i].date:
                    continue
                out.insert(i, page)
                page = None
                break
            if page:
                out.append(page)

        if reverse:
            out.reverse()
        return out
