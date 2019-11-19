import argparse

def makeBarcode(label, print_bc):
    print("^XA") # start of label
    print("^DFFORMAT^FS") # download and store format, name of format, end of field data (FS = field stop)
    print("^LH0,0") # label home position (label home = LH) 
    if print_bc:
        print("^FO400,20^AFN,60,20^FN1^FS") # AF = assign font F, field number 1 (FN1), print text at position field origin (FO) rel. to home
        print("^FO120,5^BCN,70,N,N^FN2^FS") # BC=barcode 128, field number 2, normal orientation, height 70, no interpretation line.
    else:
        ch_size="32"
        if len(label) > 42:
            ch_size = 24
        elif len(label) < 20:
            ch_size = 40
        # Scalable font ^A0N,32,32 should fit roughly 42 chars on our current labels
        print("^FO20,40^A0N,{0},{0}^FB640,1,0,C,0^FN1^FS".format(ch_size)) # FO = x,y relative field origin; A0N = scalable font height,width; FB = make into one line field block and center
    print("^XZ") # end format
    print("^XA") # start of label format
    print("^XFFORMAT^FS") # label home posision
    print("^FN1^FD{}^FS".format(label)) # this is readable
    if print_bc:
        print("^FN2^FD{}^FS".format(label)) # this is the barcode
    print("^XZ")

def main(args):
    n = args.num
    if n > 0 and n < 20:
        for _ in range(n):
            makeBarcode(args.label, args.bc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format a label with barcode for the Zebra printer")
    parser.add_argument("label", help="The text to print as barcode and text")
    parser.add_argument("-t", "--text-only", help="Skip barcode and only print label in text",
                        action="store_false", default=True, dest="bc")
    parser.add_argument("-n", "--num", help="Number of copies to print",
                        action="store", type=int, default=1, dest="num")
    args = parser.parse_args()
    main(args)
