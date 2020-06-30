/*////////////////////////////////////////////////////////////////
Permission to use, copy, modify, and distribute this program for
any purpose, with or without fee, is hereby granted, provided that
the notices on the head, the reference information, and this
copyright notice appear in all copies or substantial portions of
the Software. It is provided "as is" without express or implied
warranty.
*////////////////////////////////////////////////////////////////
#include "CommonPara.h"
#include "ParsePDB.h"
#include "ProteinSurface.h"
#include <ctime>


/*
	printf("usage: EDTSurf -i pdbname ...\n");
	printf("-o outname\n");
	printf("-t 1-MC 2-VCMC\n");
	printf("-s 1-VWS 2-SAS 3-MS 4-SES\n");
	printf("-c 1-pure 2-atom 3-chain\n");
	printf("-p probe radius [0,2.0]\n");
	printf("-f scale factor (0,20.0]\n");
	printf("-h 1-in and out 2-out 3-in\n");
	printf("output1: outname.off\n");
	printf("output2: outname.asa\n");
	printf("output3: outname-cav.pdb\n");
 */



static const char *prefix = "libEDTSurf:";

extern "C" {
	/*
	 * Calculate the surface using the given parameters, set *vertices to the
	 * list of vertices, *triangles to the list of triangles, and the
	 * corresponding number of elements in *nvertices and *ntriangles.
	 *
	 * Return 1 if success, 0 if memory error, and -1 if input file not found.
	 * In case of memory error, also and set both lists to NULL and both
	 * number of elements to 0.
	 *
	 * After using the data, the caller must call freelists() to properly free
	 * memory.
	 */
	int calc_surface(const char *inname, const int triangulation_type,
					const int surface_type, const int color_mode,
					const double probe_radius, const double scale_factor,
					const int inner_outer_surface,
					struct point **vertices, int *nvertices,
					struct triangle **triangles, int *ntriangles)
	{
		ParsePDB pp;
		ProteinSurface pps;
		int inum[4];
		double fnum[2];
		//char inname[200];
		char tpname[200];
		char filename[200];
		bool flagopt[7];
		bool bcolor;
		int i;
		clock_t remcstart, remcfinish;

		for(i = 0; i < 7; i++) {
			flagopt[i] = false;
		}
		// default values
		inum[0] = 2;    // 1-MC 2-VCMC
		inum[1] = 4;    // 1-VWS 2-SAS 3-MS 4-SES
		inum[2] = 2;    // 1-pure 2-atom 3-chain
		inum[3] = 2;    // 1-in and out 2-out 3-in
		fnum[0] = 1.4;  // probe radius
		fnum[1] = 4.00; // scale factor
		strcpy(tpname,"surfout");

		if (triangulation_type > 0) {
			flagopt[1] = true;
			if (1 == triangulation_type || 2 == triangulation_type) {
				inum[0] = triangulation_type;
			} else {
				printf("%s omit wrong value for triangulation type\n", prefix);
			}
		}

		if (surface_type > 0) {
			flagopt[2] = true;
			if (surface_type <= 4) {
				inum[1] = surface_type;
			} else {
				printf("%s omit wrong value for surface type\n", prefix);
			}
		}

		if (color_mode > 0) {
			flagopt[3] = true;
			if (color_mode <= 3) {
				inum[2] = color_mode;
			} else {
				printf("%s omit wrong value for color mode\n", prefix);
			}
		}

		if (probe_radius > 0.0) {
			flagopt[4] = true;
			if(probe_radius < 2.0) {
				fnum[0] = probe_radius;
			} else {
				printf("%s omit wrong value for probe radius\n", prefix);
			}
		}

		if (scale_factor > 0.0) {
			flagopt[5] = true;
			if(scale_factor > 0.5 && scale_factor<=20.0) {
				fnum[1] = scale_factor;
			} else {
				printf("%s omit wrong value for scale_factor\n", prefix);
				fnum[1] = 0.5;
			}
		}

		if (inner_outer_surface > 0) {
			flagopt[7] = true;
			if (inner_outer_surface <= 3) {
				inum[3] = inner_outer_surface;
			} else {
				printf("%s omit wrong value for inner/outer surface\n", prefix);
			}
		}

		printf("The specification is: input: %s, ",inname);
		if(inum[0]==1)
			printf("triangulation: MC, ");
		else printf("triangulation: VCMC, ");
		if(inum[1]==1)
			printf("surface: VWS, ");
		else if(inum[1]==2 || inum[1]==0)
			printf("surface: SAS, ");
		else if(inum[1]==4)
			printf("surface: SES, ");
		else printf("surface: MS, ");
		if(inum[2]==1)
			printf("color: pure, ");
		else if(inum[2]==2)
			printf("color: atom, ");
		else printf("color: chain, ");
		if(inum[3]==1)
			printf("surface: outer+inner, ");
		else if(inum[3]==2)
			printf("surface: outer, ");
		else printf("surface: inner, ");
		printf("radius: %6.3f, ",fnum[0]);
		printf("scale: %6.3f, ",fnum[1]);
		//printf("outname: %s\n",tpname);
		printf("Load file...\n");
		bcolor=true;
		if (!pp.loadpdb(inname)) {
			return -1;
		}
		pp.extractbb(0,-1,1);
	//	pp.PCA();
		pps.proberadius=fnum[0];
		pps.fixsf=fnum[1];
		remcstart=clock();
		if(inum[1]==1)
		{
			printf("Initialize...\n");
			pps.initpara(pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,pp.proseq,false,false);
			printf("actual boxlength %3d, box[%3d*%3d*%3d], scale factor %6.3f\n",
				pps.boxlength,pps.plength,pps.pwidth,pps.pheight,pps.scalefactor);
			printf("Build van der Waals solid\n");
			pps.fillvoxels(pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,false,pp.proseq,bcolor);
			pps.buildboundary();
			printf("Build triangulated surface\n");
			if(inum[0]==1)
				pps.marchingcubeorigin2(1);
			else if(inum[0]==2)
				pps.marchingcube(1);
		}
		else if(inum[1]==2)
		{
			printf("Initialize...\n");
			pps.initpara(pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,pp.proseq,false,true);
			printf("actual boxlength %3d, box[%3d*%3d*%3d], scale factor %6.3f\n",
				pps.boxlength,pps.plength,pps.pwidth,pps.pheight,pps.scalefactor);
			printf("Build solvent-accessible solid\n");
			pps.fillvoxels(pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,false,pp.proseq,bcolor);
			pps.buildboundary();
			printf("Build triangulated surface\n");
			if(inum[0]==1)
				pps.marchingcubeorigin2(3);
			else if(inum[0]==2)
				pps.marchingcube(3);
		}
		else if(inum[1]==3)
		{
			printf("Initialize...\n");
			pps.initpara(pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,pp.proseq,true,true);
			printf("actual boxlength %3d, box[%3d*%3d*%3d], scale factor %6.3f\n",
				pps.boxlength,pps.plength,pps.pwidth,pps.pheight,pps.scalefactor);
			printf("Build solvent-accessible solid\n");
			pps.fillvoxels(pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,true,pp.proseq,bcolor);
			pps.buildboundary();
			printf("Euclidean Distance Transform\n");
			pps.fastdistancemap(0);
			printf("Build triangulated surface\n");
			if(inum[0]==1)
				pps.marchingcubeorigin2(4);
			else if(inum[0]==2)
				pps.marchingcube(4);
		}
		else if(inum[1]==4)
		{
			printf("Initialize...\n");
			pps.initpara(pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,pp.proseq,false,true);
			printf("actual boxlength %3d, box[%3d*%3d*%3d], scale factor %6.3f\n",
				pps.boxlength,pps.plength,pps.pwidth,pps.pheight,pps.scalefactor);
			printf("Build solvent-accessible solid\n");
			pps.fillvoxels(pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,false,pp.proseq,bcolor);
			pps.buildboundary();
			printf("Euclidean Distance Transform\n");
			pps.fastdistancemap(0);
			printf("Build van der Waals solid\n");
			pps.boundingatom(false);
			pps.fillvoxelswaals(pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,false,pp.proseq,bcolor);
			printf("Build triangulated surface\n");
			if(inum[0]==1)
				pps.marchingcubeorigin2(2);
			else if(inum[0]==2)
				pps.marchingcube(2);
		}
		else if(inum[1]==0)
		{
			printf("Initialize...\n");
			pps.initpara(pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,pp.proseq,true,true);
			printf("actual boxlength %3d, box[%3d*%3d*%3d], scale factor %6.3f\n",
				pps.boxlength,pps.plength,pps.pwidth,pps.pheight,pps.scalefactor);
			printf("Build solvent-accessible solid\n");
			pps.fillvoxels(pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,true,pp.proseq,bcolor);
			pps.buildboundary();
			printf("Euclidean Distance Transform\n");
			pps.fastdistancemap(1);
			printf("Calculate Depth\n");
			pps.calcdepth(pp.numbb,pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,pp.proseq,pp.bb,true);
		}
		remcfinish=clock();
		double duration = (double)(remcfinish - remcstart)/CLOCKS_PER_SEC;
		printf("Total time %.3f seconds\n",duration);
		/*
		//depth
		if(inum[1]==0)
		{
			printf("Output atom depth and residue depth\n");
			sprintf(filename,"%s_atom.dep",tpname);
			FILE *file;
			file=fopen(filename,"wt");
			fprintf(file,"index atom# res#   depth\n");
			for(i=pp.promod[0].procha[0].chainseg.init;i<=pp.promod[0].procha[pp.promod[0].nchain].chainseg.term;i++)
			{
				fprintf(file,"%5d %5d %4d %7.3f\n",i-pp.promod[0].procha[0].chainseg.init+1,pp.proseq[i].seqno,pp.proseq[i].resno,pps.depval[i]);
			}
			fclose(file);
			sprintf(filename,"%s_res.dep",tpname);
			file=fopen(filename,"wt");
			fprintf(file,"indx res# A   depth\n");
			for(i=0;i<pp.numbb;i++)
			{
				double tsum=0;
				int tnum=0;
				for(int k=pp.bb[i].istart;k<=pp.bb[i].iend;k++)
				{
					tsum+=pps.depval[k];
					tnum++;
				}
				tsum/=double(tnum);
				fprintf(file,"%4d %4d %c %7.3f\n",i+1,pp.bb[i].resind,pp.bb[i].resid,tsum);
			}
			fclose(file);
			return 1;
		}
		*/
		//additional functions below
		pps.checkEuler();
		pps.computenorm();
		printf("No. vertices %d, No. triangles %d\n",pps.vertnumber,pps.facenumber);
		pps.calcareavolume();
		printf("Total area %.3f and volume %.3f\n",pps.sarea,pps.svolume);
		printf("Distinguish inner and outer surfaces\n");
		pps.surfaceinterior();
		printf("Calculate cavity number...\n");
		pps.cavitynumbers();
		printf("Cavity number is %d\n",pps.ncav);
		printf("Calculate cavity area and volume...\n");
		pps.cavitiesareavolume();
		printf("Cavity area %.3f and volume %.3f\n",pps.carea,pps.cvolume);
		printf("Calculate inner and outer atoms\n");
		pps.atomsinout(pp.promod[0].procha[0].chainseg.init,pp.promod[0].procha[pp.promod[0].nchain].chainseg.term,pp.proseq);

		pps.laplaciansmooth(1);
		pps.computenorm();
		printf("Output 3D model\n");
		pps.checkinoutpropa();
		//sprintf(filename,"%s.off",tpname);
		//pps.outputoff(filename);

		struct point *verts = pps.getvertices();
		struct triangle *tris = pps.gettriangles();

		if (!verts || !tris) {
			pps.freevertices(verts);
			pps.freetriangles(tris);

			*nvertices = 0;
			*ntriangles = 0;
			*vertices = NULL;
			*triangles = NULL;

			return 0;
		}

		*nvertices = pps.vertnumber;
		*ntriangles = pps.facenumber;
		*vertices = verts;
		*triangles = tris;

		return 1;
	}

	void freelists(struct point *vertices, struct triangle *triangles)
	{
		ProteinSurface pps;

		pps.freevertices(vertices);
		pps.freetriangles(triangles);
	}
}

