import argparse

def makeBarcode(label):
    print("^XA") #start of label
    print("^DFFORMAT^FS") #download and store format, name of format, end of field data (FS = field stop)
    print("^LH0,0") # label home position (label home = LH)
    print("^FO400,20^AFN,60,20^FN1^FS") #AF = assign font F, field number 1 (FN1), print text at position field origin (FO) rel. to home
    print("^FO120,5^BCN,70,N,N^FN2^FS") #BC=barcode 128, field number 2, Normal orientation, height 70, no interpreation line.
    print("^XZ") #end format
    print("^XA") #start of label format
    print("^XFFORMAT^FS") #label home posision
    print("^FN1^FD{}^FS".format(label)) #this is readable
    print("^FN2^FD{}^FS".format(label)) #this is the barcode
    print("^XZ")

def main(args):
    makeBarcode(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format a barcode for the Zebra printer")
    parser.add_argument("label", help="The text to print as barcode and text")
    args = parser.parse_args()
    main(args.label)
