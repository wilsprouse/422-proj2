def writeToHtml(grid, fp):
    #fp= open(filepath, 'w')
    fp.write("<!DOCTYPE html>\n<html>\n<head>\n")
    fp.write("<style>\n.grid-container {\n\tdisplay: grid;\n\tgrid-row-gap: 50px;\n\tbackground-color: white;\n")
    fp.write("\tgrid-template-columns:" + (' auto' * grid.cols) + ';\n}\n')
    fp.write(".grid-item{\n\tborder: .05em solid black;\n\tpadding: 2em;\n\tfont-size: 2em;\n\ttext-align: center;\n}\n")
    fp.write(".grid-wall{background-color:black}\n")

    fp.write("<body>\n<div class=\"grid-container\">\n")
    for rows in range(grid.rows):
        for cols in range(grid.cols):
            if gridp[rows,cols] == Grid.CELL_WALL:
                fp.write(f'\t<div class=\"grid-item grid-wall\"></div>\n')
            else:
                fp.write(f'\t<div class=\"grid-item\">{str(grid[rows,cols])}</div>\n')
    fp.write("""</div>\n</body>\n</html>""")
    #fp.close()
