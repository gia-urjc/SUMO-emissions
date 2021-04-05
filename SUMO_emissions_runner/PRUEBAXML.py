import xml.etree.ElementTree as et




if __name__ == "__main__":
    xtree = et.parse("1h.rou.xml")
    xroot = xtree.getroot()

    xml_vTypes = xroot.findall("vType")
    xml_trips =  xroot.findall("trip")
    for x_vT in xml_vTypes:
        print(dict(x_vT.items()))

    for x_tps in xml_trips:
        print(dict(x_tps.items()))
