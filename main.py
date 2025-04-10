import draw.create_pdf as pdf
import  pattern_generator.skeleton as skel

# create directly pdf
if __name__ == "__main__":
    # pdf.basic_pdf("test_outputs/test01.pdf")
    p = pdf.MakePdf("A2", False)




    OH = 100
    OP = 80
    DZ = 40
    Szad = 42
    m = skel.Measurements()
    m.add_chest(OH)
    m.add_waist(OP)
    m.add_back_length(DZ)
    m.add_back_width(Szad)
    print(m.get_all_measurements(1))

    position_x = 30
    position_y = 30
    sk = skel.BackSkeleton(position_x, position_y, m, 10)
    # print(sk.get_polygon(20,20))



    curve = sk.get_polygon()
    # p.add_polygon(curve, line_width=2)
    lines = sk.get_skeleton_lines()
    for l in lines.keys():
        p.add_line(lines[l][0], lines[l][1])

    # w_line = sk.get_waist_line(position_x, position_y)
    # p.add_line(w_line[0], w_line[1])
    # ch_line = sk.get_chest_line(position_x,position_y)
    # p.add_line(ch_line[0], ch_line[1])
    # n_line = sk.get_neck_line(position_x, position_y)
    # p.add_line(n_line[0], n_line[1])
    # side_line = sk.get_side_line(position_x, position_y)
    # p.add_line(side_line[0], side_line[1])
    # back_line = sk.get_back_line(position_x, position_y)
    # p.add_line(back_line[0], back_line[1])
    # c_line = sk.get_center_line(position_x, position_y)
    # p.add_line(c_line[0], c_line[1])

    p.add_mark(lines["center"][0], 5, line_width=5)
    p.add_mark(lines["center"][1], 5, line_width=5)
    # p.add_mark(60, 60, 5)
    p.add_text(lines["side"][0][1]/2, lines["side"][0][1], "Test pattern from Python", 20)

    p.save_pdf("test_outputs/test01.pdf")