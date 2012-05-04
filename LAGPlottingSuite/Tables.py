latextemplate = r"""
\begin{table}[h!]
    \centering
    %%\resizebox{%s\textwidth}{!}{
    \begin{tabular}{|l|%s|}
    \hline
    %s\hline
    \end{tabular}%%}
    \caption{%s}
    \label{%s}
\end{table}
"""

htmltemplate = r'''
<div class="CutflowTable" id="%s">
<table>
    <thead>
        <tr>
            %s
        </tr>
    </thead>
    <tbody>
        %s
    </tbody>
</table>
<p class="caption">%s</p>
</div>
'''
import unittest
import array
class Table(object):
    """A 2D table that allows for keyed inputs on both axes"""
    def __init__(self, title, caption="Table Instance"):
        super(Table, self).__init__()
        self.title = title
        self.caption = caption


        self.xlabels = []
        self.ylabels = []
        self.array = []
        
    def __getitem__(self, row_col):
        """docstring for __getitem__"""
        # return self.array[row_col[0]][row_col[1]][0]
        return -1
        
    def __setitem__(self, row_col, value):
        """docstring for __setitem__"""
        # if self.array.has_key(row_col[0]):
        #     if self.array[row_col[0]].has_key(row_col[1]):
        #         self.array[row_col[0]][row_col[1]][0] = value
        #     else:
        #         row_index = self.array[row_col[0]].items()[0][1][1]
        #         self.array[row_col[0]][row_col[1]] = [value, row_index, len(self.array[row_col[0]])]
        # else:
        #     self.array[row_col[0]] = {row_col[1] : [ value, len(self.array), 0 ] }
            
        try:
            x_index = self.xlabels.index(row_col[0])
        except ValueError:
            self.xlabels.append(row_col[0])
            x_index = self.xlabels.index(row_col[0])
            self.array.append([])
            

        try:
            y_index = self.ylabels.index(row_col[1])
        except ValueError:
            self.ylabels.append(row_col[1])
            y_index = self.ylabels.index(row_col[1])
            self.array[x_index].insert(y_index,value)
        
        print x_index, y_index, self.array[x_index][y_index]
        # self.array[x_index][y_index] = value
        
    def __str__(self):
        """docstring for __str__"""
        # for (rowId, rowValues) in sorted(self.array.items(), key= lambda x: x[0].lower()):
        return str(self.array)
            
            

        

class CutflowTable(object):
    """docstring for CutflowTable"""
    def __init__(self, title, caption="a new table"):
        super(CutflowTable, self).__init__()
        self.default_list = dict()
        self.title = title
        self.caption = caption
        

    def add(self, cut, data, value):
        """docstring for add"""
        if self.default_list.has_key(cut):
            if self.default_list[cut].has_key(data):
                self.default_list[cut][data] = value
            else:
                self.default_list[cut][data] = value
        else:
            self.default_list[cut] = {data:value}
    
    def __str__(self):
        """docstring for __str__"""
        string = ""
        k = 0
        for i in self.default_list.iterkeys():
            k += 1
            if k == 1: string+= "\t"+"\t ".join((m for m in self.default_list[i].iterkeys())) + "\n"
            string+= "%s\t"%i+ "\t ".join((str(self.default_list[i][m]) for m in self.default_list[i].iterkeys())) + "\n"
        
        string += "\nTable caption: %s\n" % self.caption
        return string
    
    def tex_ref(self):
        """docstring for tex_ref"""
        return r"tbl:%s" % self.title.replace(" ", "_").replace("$","")
        
    def latex(self, output_folder, output_folder_img, format="pdf"):
        """docstring for tabular"""
        string = ""
        length = 0
        k = 0
        for i in self.default_list.iterkeys():
            k += 1
            
            samp = self.default_list[i].keys()                
            # sorted(samp)
            if k == 1: 
                string+= "\t& "+"\t & ".join((m for m in samp)) + r" \\ \hline" + "\n"
                length = len(self.default_list[i])
            string+= "%s\t& "%i+ "\t & ".join(("$"+str(self.default_list[i][m])+"$" for m in samp)) + " \\\\ \n"

        return latextemplate % (min(1,length*0.3), length * "c", string, self.caption, self.tex_ref())
        
    def plain_text(self, output_folder, output_folder_img, format="png"):
        return self.__str__()
        
    def html(self, output_folder, output_folder_img, format="png"):
        """docstring for html"""
        string = ""
        string_hdr = ""
        length = 0
        k = 0
        for i in self.default_list.iterkeys():
            k += 1
            
            samp = self.default_list[i].keys()                
            # sorted(samp)
            if k == 1: 
                string_hdr+= "<td></td>"+" ".join(('<td>'+str(m)+'</td>' for m in samp))
            # string+= "%s\t& "%i+ "\t & ".join(("$"+str(self.default_list[i][m])+"$" for m in samp)) + " \\\\ \n"
            
            
            
            string+= "<tr><td>%s</td>" % i 
            for m in samp:
                # if self.default_list[i][m] is float:
                try:
                    string += "<td class='float'>%2.2f</td>" % float(self.default_list[i][m])
                except ValueError:
                    string += "<td class='str'>%s</td>" % self.default_list[i][m]
            
            # +" ".join(('<td>'+str(self.default_list[i][m])+'</td>' for m in samp)) + "</tr>"
            string += "</tr>"
        return htmltemplate % (self.tex_ref(), string_hdr, string, self.caption)
        

        
"""

Method	Checks that	New in
assertEqual(a, b)	a == b	 
assertNotEqual(a, b)	a != b	 
assertTrue(x)	bool(x) is True	 
assertFalse(x)	bool(x) is False	 
assertIs(a, b)	a is b	2.7
assertIsNot(a, b)	a is not b	2.7
assertIsNone(x)	x is None	2.7
assertIsNotNone(x)	x is not None	2.7
assertIn(a, b)	a in b	2.7
assertNotIn(a, b)	a not in b	2.7
assertIsInstance(a, b)	isinstance(a, b)	2.7
assertNotIsInstance(a, b)	not isinstance(a, b)	2.7

"""

class TableTests(unittest.TestCase):
    def setUp(self):
        self.table = Table("test table", "A testing table")
    
    def runTest(self):
        """docstring for runTest"""
        self.table["cut1","case1"] = "meh"
        # print self.table["cut1", "case1"]
        
        self.table["cut1","case2"] = 4
        
        self.table["cut1","case3"] = 6
        
        self.table["cut1","case4"] = 8
        self.table["cut2","case0"] = -4
        self.table["cut2","case1"] = -8
        self.table["cut2","case2"] = -16
        self.table["cut2","case3"] = -32
        self.table["cut2","case2"] = 42


        # self.assertTrue(self.table['cut2', 'case2'] == 42)

        print self.table


        
        


if __name__ == '__main__':
    unittest.main()# c = CutflowTable()
# 
# c.add("cut1", "data", 12)
# c.add("cut2", "data", 5)
# c.add("cut3", "data", 1)
# 
# c.add("cut1", "bg", 12)
# c.add("cut2", "bg", 5)
# c.add("cut3", "bg", 1)
# 
# 
# c.add("cut1", "signal1", 1322)
# c.add("cut2", "signal1", 523)
# c.add("cut3", "signal1", 13)
# 
# c.add("cut1", "signal2", 1322)
# c.add("cut2", "signal2", 523)
# c.add("cut3", "signal2", 13)
# 
# print c.tabular()