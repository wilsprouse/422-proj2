import Grid
#
Bob= Grid.Grid(2,2)
#Bob[0,0].set('z')
#Bob[0,1].set('y')
#Bob[1,0].set('a')
#Bob[1,1].set('b')

fp = open('showGrid.html', 'w')
fp.write("""<!DOCTYPE html>
<html>
<head>
<style>
.grid-container {
    display: grid;
    grid-row-gap: 50px;
    grid-template-columns: """
    +('auto '* Bob.cols) + ';'+
    """\tbackground-color: #2196F3;
        padding: 10px;
}
.grid-item{
    background-color:rgba(255, 255, 255, 0.8);
    border: 1 px solid rgba(0, 0, 0, 0.8);
    padding: 20px;
    font-size: 30px;
    text-align: center;
}
</style>
</head>""")
fp.write("""<body><div class="grid-container">\n""")
for rows in range(Bob.rows):
    for cols in range(Bob.cols):
        fp.write(f'\t<div class= grid-item>{str(Bob[rows,cols])}</div>\n')
fp.write("""</div>\n</body>\n</html>""")
fp.close()
