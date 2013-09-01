/*
 Author: Joel Gruselius
 Version: 2012-12-21
 Description: Various simple but useful methods for nucleotide sequences
 to be used in a terminal.
*/

import java.util.HashMap;
import java.util.Map;

/*
 TODO:
 -Convert String nucleotide sequence to byte array
 -Handle sequences as streams instead of single String/array
*/
public class SeqTools {
	private enum Mode { INFO, REVERSE, COMPLEMENT, REVERSECOMPLEMENT, SEARCH, HELP }
	private static final HashMap<Character, Character> COMPLEMENT = createMap();
	public static HashMap<Character, Character> createMap() {
		HashMap<Character, Character> map = new HashMap<Character, Character>();
		map.put('A', 'T');
		map.put('T', 'A');
		map.put('C', 'G');
		map.put('G', 'C');
		return map;
	}

	public static Mode clParse(String[] args) {
		Mode mode = Mode.HELP;
		try {
			mode = Mode.valueOf(args[0].toUpperCase());
		} catch(IllegalArgumentException e) {}
		return mode;
	}

	public static void main(String[] args) {
		long t = System.currentTimeMillis();
		Mode mode = clParse(args);
		String seq = args[1];
		String res = null;
		switch(mode) {
			case INFO:
				res = stats(seq);
				break;
			case REVERSE:
				res = reverse(seq);
				break;
			case COMPLEMENT:
				res = complement(seq);
				break;
			case REVERSECOMPLEMENT:
				res = reverseComplement(seq);
				break;
			case SEARCH:
				res = search(seq, args[2]);
				break;
			case HELP:
				res = help();
				break;
			default:
				res = help();
				break;
		}
		for(int i = 0, n = args.length; i < n; i++) {
			// System.out.println(reverseComplement(args[i]));
		}
		System.out.println(res);
		System.out.println("Time: " + (System.currentTimeMillis()-t) + " ms");
	}

	public static String help() {
		return "Usage:\n\tjava <command> <sequence>\n";
	}

	public static byte[] stringToByteArray(String str) {
		byte[] b = new byte[str.length()];
		for (int i = 0; i < b.length; i++) {
			b[i] = (byte) str.charAt(i);
		}
		return b;
	}

	public static String stats(String seq) {
		HashMap<Character, Integer> counts = new HashMap<Character, Integer>();
		counts.put('A', 0);
		counts.put('T', 0);
		counts.put('C', 0);
		counts.put('G', 0);
		float n = seq.length();
		char c;
		for(int i = 0; i < n; i++) {
			c = seq.charAt(i);
			counts.put(c, counts.get(c)+1);
		}
		String stats = "Length: " + n + ", " +
			"A: " + 100*counts.get('A')/n + "%, " +
			"T: " + 100*counts.get('T')/n + "%, " +
			"C: " + 100*counts.get('C')/n + "%, " +
			"G: " + 100*counts.get('G')/n + "%, ";
		return stats;
	}

	// Reverse using StringBuffer:
	public static String reverse(String seq) {
		StringBuffer sb = new StringBuffer(seq);
		return sb.reverse().toString();
	}

	 // Reverse using char array:
	public static String reverse2(String seq) {
		char[] arr = seq.toCharArray();
		int len = arr.length;
		char[] rev = new char[len];
		for(int i = 0; i < len; i++) {
			rev[i] = arr[len-i-1];
		}
		return String.valueOf(rev);
	}

	// Complement using StringBuffer:
	public static String complement(String seq) {
		int len = seq.length();
		StringBuffer sb1 = new StringBuffer(seq);
		StringBuffer sb2 = new StringBuffer();
		for(int i = 0; i < len; i++) {
			sb2.append(COMPLEMENT.get(sb1.charAt(i)));
		}
		return sb2.toString();
	}

	// Complement using char array:
	public static String complement2(String seq) {
		int len = seq.length();
		char[] arr = seq.toCharArray();
		char[] compl = new char[len];
		for(int i = 0; i < len; i++) {
			compl[i] = COMPLEMENT.get(arr[i]);
		}
		return String.valueOf(compl);
	}

	// Reverse complement using StringBuffer:
	public static String reverseComplement(String seq) {
		return complement(reverse(seq));
	}

	// Reverse complement using char array:
	public static String reverseComplement2(String seq) {
		char[] arr = seq.toCharArray();
		int len = arr.length;
		char[] rev = new char[len];
		for(int i = 0; i < len; i++) {
			rev[i] = COMPLEMENT.get(arr[len-i-1]);
		}
		return String.valueOf(rev);
	}

	public static void test(String s) {
		byte[] b = stringToByteArray(s);
		for(int i = 0; i < b.length; i++) {
			System.out.println(b[i]);
		}
	}

	public static String search(String seq, String query) {
		String matchStr = "";
		String[] split = seq.split(query);
		if(split.length > 1) {
			matchStr = split[0].toLowerCase() + "|" + query.toUpperCase() +
				"|" + split[1].toLowerCase();
		}
		return matchStr;
	}
 }
/*
 public class SeqToolsOption {
 	private enum Mode { INFO, REVERSE, COMPLEMENT, REVERSECOMPLEMENT, SEARCH, HELP }
 	private Mode mode;
 	private String seq;
 	private String other;

 	public SeqToolsOption(Mode mode, String seq, String other) {
 		this.mode = mode;
 		this.seq = seq;
 		this.other = other;
 	}
 }
 */