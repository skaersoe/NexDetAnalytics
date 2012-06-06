'''
LaTeX Tables


from LAGPlottingSuite.Tables import CutflowTable

mytable = CutflowTable("unique_tag","caption string")
mytable.add("row caption","column caption","value")
mytable.save_file("table.tex")




'''




stringtemplate = '''
%s\n
%s\n
'''
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
import operator

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
        self.cuts = []
        self.samples = []
        

    def add(self, cut, data, value):
        """docstring for add"""
        
        if not cut in self.cuts:
            self.cuts.append(cut)
        
        if not data in self.samples:
            self.samples.append(data)
        
        
        
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
        length = 0
        k = 0
        for i in self.cuts:
            k += 1
            if k == 1: 
                string+= "\t| "+"\t | ".join((m for m in self.samples)) + "\n"
            
            
            length = len(self.samples)
            
            string+= "%s\t" % i
            for m in self.samples:
                try:
                    string += "\t | %s" % self.default_list[i][m]
                except:
                    string += "\t  |" 
            string +=  "\n"

        return stringtemplate % (string, self.caption)

            
    def tex_ref(self):
        """docstring for tex_ref"""
        return r"tbl:%s" % self.title.replace(" ", "_").replace("$","")
        
    def save_file(self, filename):
        """docstring for save_file"""
        with open(filename, "w") as f:
            f.write(self.latex("", ""))
            
    def latex(self, output_folder, output_folder_img, timestamp="", format="pdf"):
        """docstring for tabular"""
        string = ""
        length = 0
        k = 0
        for i in self.cuts:
            k += 1
            if k == 1: 
                string+= "\t& "+"\t & ".join((m for m in self.samples)) + r" \\ \hline" + "\n"
            
            
            length = len(self.samples)
            
            string+= "%s\t" % i
            for m in self.samples:
                try:
                    string += "\t & %s" % self.default_list[i][m]
                except:
                    string += "\t  &" 
            string +=  r"\\" + "\n"

        return latextemplate % (min(1,length*0.3), length * "c", string, self.caption, self.tex_ref())
        
    def plain_text(self, output_folder, output_folder_img, timestamp="", format="png"):
        return self.__str__()
        
    def html(self, output_folder, output_folder_img, timestamp="", format="png"):
        """docstring for html"""
        string = ""
        string_hdr = ""
        length = 0
        k = 0


        for i in self.cuts:
            k += 1
            
            samp = self.default_list[i].keys()                
            # sorted(samp, key=lambda x: )
            
            if k == 1: 
                string_hdr+= "<td></td>"+" ".join(('<td>'+str(m)+'</td>' for m in self.samples)) + "\n"
            # string+= "%s\t& "%i+ "\t & ".join(("$"+str(self.default_list[i][m])+"$" for m in samp)) + " \\\\ \n"
            
            
            
            string+= "<tr>\n<td>%s</td>" % i 

            for m in self.samples:
                # if self.default_list[i][m] is float:
                try:
                    string += "<td class='float'>%2.4f</td>" % self.default_list[i][m]  + "\n"
                except:
                    string += "<td class='empty'>-</td>"+ "\n"
            
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
        self.table = CutflowTable("test table", "A testing table")
    
    def runTest(self):
        """docstring for runTest"""
        self.table.add("cut1","case1", "meh" )
        self.table.add("cut1","case2", 4     )
        self.table.add("cut1","case3", 3     )
        self.table.add("cut1","case4", 8     )
        
        self.table.add("cut2","case0", -4    )
        self.table.add("cut2","case1", -8    )
        self.table.add("cut2","case2", -16   )
        self.table.add("cut2","case3", -32   )
        self.table.add("cut2","case2", 42    )
        self.table.add("cut3","case1", -8    )
        self.table.add("cut3","case2", -16   )


        # self.assertTrue(self.table['cut2', 'case2'] == 42)

        print self.table


        print self.table.latex( "", "", format="pdf")
        print self.table.html( "", "", format="pdf")

        
        
if __name__ == '__main__':
    unittest.main()
