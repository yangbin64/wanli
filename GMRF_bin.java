package bayesianOptimization;

import org.apache.commons.math3.linear.*;
import org.apache.commons.math3.distribution.*;
import java.util.*;
import java.io.*;

public class GMRF_bin {
	
	class Feedback {
		double count;
		double sum;
		double prob;

		public Feedback() {
			count = 0;
			sum = 0;
		}
		
		public Feedback(double count, double sum) {
			this.count = count;
			this.sum = sum;
			this.calcprob();
		}
		
		public void addfeedback(int fb) {
			count++;
			sum += fb;
			this.calcprob();
		}
		
		void calcprob() {
			double r = (sum+0.07)/(count+1);
			prob = 1.0/(1.0+Math.exp(-r));
		}
	}
	
	class Sampler {
		int idx;
		HashSet<Integer> neighbors = new HashSet<Integer>();
		double average;
		double std;
		double sample;
		
		public Sampler(int idx) {
			this.idx = idx;
		}
		
		public void initial() {
			for (int i=0; i<Laplacian.length; i++) {
				if (i!=idx && Laplacian[idx][i]==-1.0) {
					neighbors.add(i);
				}
			}
		}
		
		public void sample() {
			double count = 1;
			double sum = 0;
			
			for (Iterator<Integer> it=neighbors.iterator(); it.hasNext(); ) {
				int i = it.next();
				count = count+1*4;
				sum = sum + sampler_list[i].sample*4;
			}
			
			count = count+fb_list[idx].count*25;
			sum = sum+fb_list[idx].sum*25;
			
			average = sum/count;
			std = 1.0/Math.sqrt(count);
			
			NormalDistribution nd = new NormalDistribution();
			sample = average + nd.sample()*std;
		}
	}
	
	int SIZE = 11;
	int DIM = 3;
	String filename_input = "C:\\Analysis\\20_input\\input" + DIM + ".csv";
	String filename_output = "C:\\Analysis\\30_trainTS\\log" + DIM + ".csv";
	String bandit_type = "UCB";
	
	double[][] Laplacian;
	double ALPHA = 1.0;
	
	HashSet<Integer> ValidIndex;
	HashSet<Integer> InvalidIndex;
	
	Feedback[] fb_list;
	double[] performance_list;
	Sampler[] sampler_list;
	
	public void setparameter(String[] args) {
		if (args.length>=1) {
			SIZE = Integer.valueOf(args[0]);
		}
		
		if (args.length>=2) {
			DIM = Integer.valueOf(args[1]);
		}
		
		if (args.length>=3) {
			filename_input = args[2];
		}
		
		if (args.length>=4) {
			filename_output = args[3];
		}
		
		if (args.length>=5) {
			bandit_type = args[4];
		}
		
		System.out.println("[SIZE] " + SIZE);
		System.out.println("[DIM] " + DIM);
		System.out.println("[INPUT] " + filename_input);
		System.out.println("[OUTPUT] " + filename_output);
		System.out.println("[BANDIT] " + bandit_type);
	}
	
	public void initialperformance2(String filename) {
		int len = (int)Math.pow(SIZE,DIM);
		performance_list = new double[len];
		
		try {
			FileReader fr = new FileReader(filename);
			BufferedReader br = new BufferedReader(fr);
			String s;
			
			while ((s=br.readLine())!=null) {
				String[] ss = s.split(",");
				int s1 = Integer.valueOf(ss[0]);
				int s2 = Integer.valueOf(ss[1]);
				double y = Double.valueOf(ss[2]);
				int index = s1*SIZE + s2;
				performance_list[index] = y;
			}
			
			fr.close();
		} catch (Exception e) {
			System.out.println(e);
		}
	}
	
	public void initialperformance3(String filename) {
		int len = (int)Math.pow(SIZE,DIM);
		performance_list = new double[len];
		
		try {
			FileReader fr = new FileReader(filename);
			BufferedReader br = new BufferedReader(fr);
			String s;
			
			while ((s=br.readLine())!=null) {
				String[] ss = s.split(",");
				int s1 = Integer.valueOf(ss[0]);
				int s2 = Integer.valueOf(ss[1]);
				int s3 = Integer.valueOf(ss[2]);
				double y = Double.valueOf(ss[3]);
				int index = s1*SIZE*SIZE + s2*SIZE + s3;
				performance_list[index] = y;
			}
			
			fr.close();
		} catch (Exception e) {
			System.out.println(e);
		}
	}
	
	public void initialperformance4(String filename) {
		int len = (int)Math.pow(SIZE,DIM);
		performance_list = new double[len];
		
		try {
			FileReader fr = new FileReader(filename);
			BufferedReader br = new BufferedReader(fr);
			String s;
			
			while ((s=br.readLine())!=null) {
				String[] ss = s.split(",");
				int s1 = Integer.valueOf(ss[0]);
				int s2 = Integer.valueOf(ss[1]);
				int s3 = Integer.valueOf(ss[2]);
				int s4 = Integer.valueOf(ss[3]);
				double y = Double.valueOf(ss[4]);
				int index = s1*SIZE*SIZE*SIZE + s2*SIZE*SIZE + s3*SIZE + s4;
				performance_list[index] = y;
			}
			
			fr.close();
		} catch (Exception e) {
			System.out.println(e);
		}
	}
	
/*	public void initialperformance() {
		int len = (int)Math.pow(SIZE,DIM);
		performance_list = new double[len];
		int index = 0;
		for (int s1=0; s1<SIZE; s1++) {
			for (int s2=0; s2<SIZE; s2++) {
				for (int s3=0; s3<SIZE; s3++) {
					double e = (-(s1-3.0)*(s1-3.0)-(s2-5.0)*(s2-5.0)-(s3-6.0)*(s3-6.0))/20;
					double value = Math.exp(e);
					performance_list[index] = value;
					index++;
				}
			}
		}
	}*/
	
	public double[][] construct(double[][] base) {
		int len = base.length;
		int len_new = len*SIZE;
		double[][] base_new = new double[len_new][len_new];
		
		for (int s1=0; s1<SIZE; s1++) {
			int x1 = s1*len;
			for (int s2=0; s2<SIZE; s2++) {
				int x2 = s2*len;
				if (s1==s2) {
					// copy base to sub matrix from (x1,x2)
					for (int l1=0; l1<len; l1++) {
						for (int l2=0; l2<len; l2++) {
							base_new[x1+l1][x2+l2] = base[l1][l2];
						}
					}
				} else if (Math.abs(s1-s2)==1) {
					// set negative identity matrix
					for (int l=0; l<len; l++) {
						base_new[x1+l][x2+l] = -1;
					}
				}
			}
		}
		
		return base_new;
	}
	
	public void construct() {
		//int len = SIZE^DIM;
		//Laplacian = new double[len][len];
		
		Laplacian = new double[1][1];
		//printmatrix(Laplacian);
		for (int d=0; d<DIM; d++) {
			Laplacian = construct(Laplacian);
			//printmatrix(Laplacian);
		}
		
		int len = Laplacian.length;
		for (int l1=0; l1<len; l1++) {
			double sum = 0;
			for (int l2=0; l2<len; l2++) {
				sum = sum - Laplacian[l1][l2];
			}
			Laplacian[l1][l1] = sum;
			//System.out.print(" " + (int)Math.round(sum));
		}
	}
	
	public void printmatrix(double[][] m) {
		int len = m.length;
		
		for (int x1=0;x1<len; x1++) {
			for (int x2=0;x2<len; x2++) {
				double value_d = m[x1][x2];
				int value_i = (int)Math.round(value_d);
				System.out.print(" " + value_i);
			}
			System.out.println();
		}
	}
	
	public void printmatrix(RealMatrix m) {
		for (int r = 0; r < m.getRowDimension(); r++) {
	        for (int c = 0; c < m.getColumnDimension(); c++) {
	        	double value = Math.round(m.getEntry(r, c));
	        	int value_i = (int)value;
	        	System.out.print(" " + value_i);
	        }
	        System.out.println();
	    }
	}
	
	public void printdiagonal(RealMatrix m) {
		for (int r = 0; r < m.getRowDimension(); r++) {
        	System.out.print(" " + m.getEntry(r, r));
	    }
        System.out.println();
	}
	
	public void eigendecomposition(double[][] vecMatrix) {
		RealMatrix m = new Array2DRowRealMatrix(vecMatrix);
		EigenDecomposition dec = new EigenDecomposition(m);
		RealMatrix D = dec.getD();
		printdiagonal(D);
		RealMatrix V = dec.getV();
		//printmatrix(V);
		
		RealMatrix VT = V.transpose();
		RealMatrix VDVT = V.multiply(D).multiply(VT);
		//printmatrix(VDVT);
	}
	
	public RealMatrix matrixinverse(double[][] vecMatrix) {
		RealMatrix m = new Array2DRowRealMatrix(vecMatrix);
		EigenDecomposition dec = new EigenDecomposition(m);
		RealMatrix D = dec.getD();
		RealMatrix V = dec.getV();
		
		int len = vecMatrix.length;
		for (int l=0; l<len; l++) {
			double value = D.getEntry(l, l);
			D.setEntry(l, l, 1.0/value);
		}
		RealMatrix VT = V.transpose();
		RealMatrix INV = V.multiply(D).multiply(VT);
		
		return INV;
	}
	
	public void getvalidindex() {
		ValidIndex = new HashSet<Integer>();
		InvalidIndex = new HashSet<Integer>();
		
		int len = Laplacian.length;
		fb_list = new Feedback[len];
		for (int l=0; l<len; l++) {
			double value = Laplacian[l][l];
			
			if (value > DIM*2-0.01) {
				ValidIndex.add(l);
				fb_list[l] = new Feedback();
			} else {
				InvalidIndex.add(l);
				fb_list[l] = new Feedback(1, 0.5);
			}
		}
	}
	
	public int UCB() {
		int len = Laplacian.length;
		double[][] matrixA = new double[len][len];
		for (int l1=0; l1<len; l1++) {
			for (int l2=0; l2<len; l2++) {
				matrixA[l1][l2] = Laplacian[l1][l2];
			}
		}
		double[] vectorb = new double[len];
		
		for (int l=0; l<len; l++) {
			double count = fb_list[l].count;
			double sum = fb_list[l].sum;
			matrixA[l][l] += count;
			vectorb[l] = sum;
		}
		
		RealMatrix INV = matrixinverse(matrixA);
		double[] vectorb_new = INV.operate(vectorb);
		
		int trial = -1;
		double ucb_largest = -10000;
		boolean b = false;
		for (Iterator<Integer> it=ValidIndex.iterator(); it.hasNext(); ) {
			int index = it.next();
			double ave = vectorb_new[index];
			double std = Math.sqrt(INV.getEntry(index, index));
			double ucb = ave + std*ALPHA;
			if (b)
				System.out.println("" + index + ": " + ave + ", " + std);
			if (ucb>ucb_largest) {
				trial = index;
				ucb_largest = ucb;
			}
		}
		
		return trial;
	}
	
	public int getfeedback(int trial) {
		double performance = performance_list[trial];
		BinomialDistribution b = new BinomialDistribution(1, performance);
		int fb = b.sample();
		System.out.println("" + trial + ": " + performance + ", " + fb);
		
		int[] idx = new int[4];
		int t = trial;
		for (int i=0; i<4; i++) {
			idx[i] = t%SIZE;
			t = (t-idx[i])/SIZE;
		}
		
		try {
			FileWriter fw = new FileWriter(filename_output, true);
			if (DIM==2) {
				fw.write("" + trial + "," + idx[1] + "," + idx[0] + "," + performance + "," + fb + "\n");
			} else if (DIM==3) {
				fw.write("" + trial + "," + idx[2] + "," + idx[1] + "," + idx[0] + "," + performance + "," + fb + "\n");
			} else if (DIM==4) {
				fw.write("" + trial + "," + idx[3] + "," + idx[2] + "," + idx[1] + "," + idx[0] + "," + performance + "," + fb + "\n");
			}
			fw.close();
		} catch (Exception e) {
			System.out.println(e);
		}
		
		return fb;
	}
	
	public void initialsamplers() {
		int len = Laplacian.length;
		sampler_list = new Sampler[len];
		for (int l=0; l<len; l++) {
			sampler_list[l] = new Sampler(l);
			sampler_list[l].initial();
		}
	}
	
	public int TS() {
		int len = Laplacian.length;
		
		for (int t=0; t<100; t++) {
			for (int l=0; l<len; l++) {
				sampler_list[l].sample();
			}
		}
		
		int trial = -1;
		double ts_largest = -10000;
		double average = 0;
		double std = 0;
		for (Iterator<Integer> it=ValidIndex.iterator(); it.hasNext(); ) {
			int index = it.next();
			double ts = sampler_list[index].sample;
			if (ts>ts_largest) {
				trial = index;
				ts_largest = ts;
				average = sampler_list[index].average;
				std = sampler_list[index].std;
			}
		}
		
		System.out.print("" + average + ", " + std + ", " + ts_largest + " === ");
		return trial;
	}
	
	public void runUCB() {
		System.out.println("Starting...");
		if (DIM == 2) {
			initialperformance2(filename_input);
		} else if (DIM == 3) {
			initialperformance3(filename_input);
		} else if (DIM == 4) {
			initialperformance4(filename_input);
		} else {
			System.out.println("DIM is error!");
			return;
		}
		
		System.out.println("Constructing...");
		construct();
		//printmatrix(Laplacian);
		System.out.println("Eigen decomposition...");
		eigendecomposition(Laplacian);
		getvalidindex();
		
		System.out.println(ValidIndex);
		System.out.println(ValidIndex.size());
		System.out.println(InvalidIndex);
		System.out.println(InvalidIndex.size());
		
		try {
			FileWriter fw = new FileWriter(filename_output);
			fw.close();
		} catch (Exception e) {
			System.out.println(e);
		}
		for (int n=0; n<1000; n++) {
			if (n==600) {
				System.out.println(n);
			}
			int trial = UCB();
			int fb = getfeedback(trial);
			fb_list[trial].addfeedback(fb);
		}
	}
	
	public void runTS() {
		System.out.println("Starting...");
		if (DIM == 2) {
			initialperformance2(filename_input);
		} else if (DIM == 3) {
			initialperformance3(filename_input);
		} else if (DIM == 4) {
			initialperformance4(filename_input);
		} else {
			System.out.println("DIM is error!");
			return;
		}
		
		System.out.println("Constructing...");
		construct();
		//printmatrix(Laplacian);
		//System.out.println("Eigen decomposition...");
		//eigendecomposition(Laplacian);
		getvalidindex();
		
		System.out.println(ValidIndex);
		System.out.println(ValidIndex.size());
		System.out.println(InvalidIndex);
		System.out.println(InvalidIndex.size());
		
		initialsamplers();
		
		try {
			FileWriter fw = new FileWriter(filename_output);
			fw.close();
		} catch (Exception e) {
			System.out.println(e);
		}
		for (int n=0; n<1000; n++) {
			if (n==600) {
				System.out.println(n);
			}
			int trial = TS();
			int fb = getfeedback(trial);
			fb_list[trial].addfeedback(fb);
		}
	}
	
	public static void main(String[] args) {
		GMRF_bin g = new GMRF_bin();
		g.setparameter(args);
		if (g.bandit_type.equalsIgnoreCase("UCB")) {
			g.runUCB();
		} else if (g.bandit_type.equalsIgnoreCase("TS")) {
			g.runTS();
		} else {
			System.out.println("BANDIT TYPE is invalid! (" + g.bandit_type + ")");
		}
	}

}
