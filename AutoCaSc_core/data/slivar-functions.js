var config = {min_GQ: 20, min_AB: 0.20, min_DP: 20}
// hi quality variants
function hq(kid, mom, dad) {
  return hq1(kid) && hq1(mom) && hq1(dad)
}

function hq1(sample) {
  if (sample.unknown || sample.GQ < config.min_GQ) { return false; }
  if (sample.DP < config.min_DP) { return false; }
  if (sample.hom_ref){
      return sample.AB < 0.05 // was 0.02
  }
  if(sample.het) {
      return sample.AB >= config.min_AB && sample.AB <= (1 - config.min_AB)
  }
  return sample.AB > 0.95 // was 0.98
}




function hq_or_missing(sample) {
  if (sample.unknown) { return true; }
  if (sample.GQ < config.min_GQ) { return false; }
  if (sample.DP < config.min_DP) { return false; }
  if (sample.hom_ref){
      return sample.AB < 0.05 // was 0.02
  }
  if(sample.het) {
      return sample.AB >= config.min_AB && sample.AB <= (1 - config.min_AB)
  }
  return sample.AB > 0.95 // was 0.98
}

function unknown_inheritance(kid, mom, dad, chromosome, gnomad_popmax_af, dominant_af_max, ar_af_max, nhomalt, x_recessive_af_max){
  if(kid.hom_ref){return false;}
  if(!(mom.unknown || dad.unknown)){ return false; }
  if(!(hq1(kid) && hq_or_missing(mom) && hq_or_missing(dad))){ return false; }
  if(!((chromosome == "Y") || (chromosome == "chrY"))) {
    if(!((kid.sex == "male") && ((chromosome == "X") || (chromosome == "chrX")))) {
      if(dad.unknown) {
        if(!mom.unknown) {
          if(mom.affected) {
            if(dad.affected) {
               if(mom.hom_ref) {return false;}
               if(mom.het && (gnomad_popmax_af >= dominant_af_max)) {return false;}
               if(mom.hom_alt) {
                 if(kid.het && (gnomad_popmax_af >= dominant_af_max)) {return false;}
                 if(kid.hom_alt && (gnomad_popmax_af >= ar_af_max)) {return false;}
               }
            }
            if(!dad.affected) {
                if(mom.hom_ref) {return false;}
                if(kid.het && (gnomad_popmax_af >= dominant_af_max)) {return false;}
                if(kid.hom_alt && mom.het) {return false;}
                if(kid.hom_alt && (gnomad_popmax_af >= ar_af_max)) {return false;}
            }
          }
          if(!mom.affected) {
            if(dad.affected) {
                if(!mom.hom_ref) {return false;}
                if(mom.hom_ref) {
                    if(kid.het && (gnomad_popmax_af >= dominant_af_max)) {return false;}
                    if(kid.hom_alt) {return false;}
                }
            }
            if(!dad.affected) {
                if(mom.hom_alt) {return false;}
                if(mom.hom_ref && (gnomad_popmax_af >= dominant_af_max)) {return false;}
                if(mom.hom_ref && kid.hom_alt) {return false;}
                if(mom.het && kid.het) {return false;}
                if(mom.het && (gnomad_popmax_af >= ar_af_max)) {return false;}
            }
          }
        }
        if(mom.unknown) {
            if(kid.het && (gnomad_popmax_af >= dominant_af_max)) {return false;}
            if(kid.hom_alt && (gnomad_popmax_af >= ar_af_max)) {return false;}
        }
      }
      if(mom.unknown) {
        if(mom.affected) {
            if(dad.affected) {
                if(dad.hom_ref) {return false;}
                if(kid.het && (gnomad_popmax_af >= dominant_af_max)) {return false;}
                if(kid.hom_alt && (gnomad_popmax_af >= ar_af_max)) {return false;}
            }
            if(!dad.affected) {
                if(dad.hom_alt) {return false;}
                if(dad.hom_ref && kid.hom_alt) {return false;}
                if(dad.hom_ref && kid.het && (gnomad_popmax_af >= dominant_af_max)) {return false;}
                if(dad.het && kid.het) {return false;}
                if(dad.het && kid.hom_alt && (gnomad_popmax_af >= ar_af_max)) {return false;}
            }
        }
        if(!mom.affected) {
            if(dad.affected) {
                if(kid.het) {
                    if(dad.hom_ref) {return false;}
                    if(gnomad_popmax_af >= dominant_af_max) {return false;}
                }
                if(kid.hom_alt) {
                    if(dad.hom_alt && (gnomad_popmax_af >= ar_af_max)) {return false;}
                    if(!dad.hom_alt) {return false;}
                }
            }
            if(!dad.affected) {
                if(kid.hom_alt) {
                    if(dad.het && (gnomad_popmax_af >= ar_af_max)) {return false;}
                    if(!dad.het) {return false;}
                }
                if(kid.het) {
                    if(dad.hom_ref && (gnomad_popmax_af >= dominant_af_max)) {return false;}
                    if(!dad.hom_ref) {return false;}
                }
            }
        }
      }
  }
    if((kid.sex == "male") && ((chromosome == "X") || (chromosome == "chrX"))) {
    if(!kid.hom_alt) {return false;}
    if(dad.unknown) {
        if(!mom.unknown) {
            if(mom.affected) {
                if(!mom.hom_alt) {return false;}
                if(gnomad_popmax_af >= x_recessive_af_max) {return false;}
            }
            if(!mom.affected) {
                if(!mom.het) {return false;}
                if(gnomad_popmax_af >= x_recessive_af_max) {return false;}
           }
        }
        if(mom.unknown) {
            if(gnomad_popmax_af >= x_recessive_af_max) {return false;}
        }
    }
    if(mom.unknown) {
        if(dad.affected) {
            if(!dad.hom_alt) {return false;}
            if(gnomad_popmax_af >= x_recessive_af_max) {return false;}
        }
        if(!dad.affected) {
            if(dad.hom_alt) {return false;}
            if(gnomad_popmax_af >= x_recessive_af_max) {return false;}
        }
    }
  }
  }
  if((chromosome == "Y") || (chromosome == "chrY")) {
    if(!(kid.sex == "male")) {return false;}
    if(gnomad_popmax_af >= dominant_af_max) {return false;}
  }
  return true;
}




function hqrv(variant, INFO, af_cutoff) {
  // hi-quality, rare variant.
  return INFO.gnomad_popmax_af < af_cutoff && variant.FILTER == 'PASS'
}

function denovo(kid, mom, dad){
  // check genotypes match expected pattern
  if(!(kid.het && mom.hom_ref && dad.hom_ref)){ return false; }
  if(!hq(kid, mom, dad)){ return false; }
  return ((mom.AD[1] + dad.AD[1]) < 2)
}

function x_denovo(kid, mom, dad) {
  if(!(kid.alts >= 1 && mom.hom_ref && dad.hom_ref && kid.AB > 0.3)){ return false; }
  if(!hq(kid, mom, dad)) { return false; }
  if(kid.sex != 'male') { return false; }
  return ((mom.AD[1] + dad.AD[1]) < 2);
}

function uniparent_disomy(kid, mom, dad) {
  if(kid.DP < 10 || mom.DP < 10 || dad.DP < 10) { return false; }
  if(kid.GQ < 20 || mom.GQ < 20 || dad.GQ < 20) { return false; }
  if(!(hq1(kid) && hq1(mom) && hq1(dad))){ return false; }
  return (kid.alts == 0 || kid.alts == 2) && ((mom.alts == 2 && dad.alts == 0) || (mom.alts == 0 && dad.alts == 2));
}

function recessive(kid, mom, dad) {
  return kid.hom_alt && mom.het && dad.het && hq(kid, mom, dad)
}

function x_recessive(kid, mom, dad) { 
  return (mom.het && kid.AB > 0.75 && dad.hom_ref && kid.alts >= 1 && hq(kid, mom, dad)
              && kid.sex == 'male' && mom.AB > config.min_AB && mom.AB < (1 - config.min_AB)
              )
}

// heterozygous (1 side of compound het)
function solo_ch_het_side(sample) {
  return sample.het && hq1(sample)
}

function comphet_side(kid, mom, dad) {
  return kid.het && (solo_ch_het_side(mom) != solo_ch_het_side(dad)) && mom.alts != 2 && dad.alts != 2 && solo_ch_het_side(kid) && hq1(mom) && hq1(dad);
}

// assume that mom and kid are affected.
function fake_auto_dom(kid, mom, dad) {
  return kid.het && mom.het && dad.hom_ref && hq(mom, dad, kid)
}

function trio_autosomal_dominant(kid, dad, mom) {
  // affected samples must be het.
  if(!(kid.affected == (kid.alts == 1) && mom.affected == (mom.alts == 1) && dad.affected == (dad.alts == 1))) { return false; }
  return kid.affected && hq(kid, dad, mom)
}


// functions to be use with --family-expr

function segregating_dominant_x(s) {
  // this is an internal function only called after checking sample quality and on X
  if(!s.affected) { return s.hom_ref }

  if(s.sex == "male") {
    for(var i=0; i < s.kids.length; s++) {
      var kid = s.kids[i];
      // kids of affected dad must be affected.
      if(!kid.affected) { return false; }
    }
    // mom of affected male must be affected.
    if(("mom" in s) && !(s.mom.affected && s.mom.het)){ return false; }
    if(("mom" in s) && !hq1(mom)){ return false; }
    if(("dad" in s) && !hq1(dad)){ return false; }

    return (s.hom_alt || s.het) && hq1(s)
  }
  if(s.sex != "female"){return false; }
  // this block enforces inherited dominant, but not find de novos
  if(("mom" in s) || ("dad" in s)) {
    if(!((("mom" in s) && s.mom.affected && s.mom.het) || (s.dad && s.dad.affected))) { return false;}
    if(("dad" in s) && !hq1(s.dad)){ return false; }
    if(("mom" in s) && !hq1(s.mom)){ return false; }
  }
  return s.het && hq1(s)
}

function hom_ref(s) {
	return s && s.hom_ref && hq1(s)
}

function hom_ref_parent(s) {
	return ("dad" in s) && s.dad.hom_ref && ("mom" in s) && s.mom.hom_ref
}

function segregating_dominant(s) {
  if(!hq1(s)){ return false; }
  if(variant.CHROM == "chrX" || variant.CHROM == "X") { return segregating_dominant_x(s); }
  if (s.affected) {
     return s.het
  }
  return s.hom_ref && s.AB < 0.01
}


function segregating_recessive_x(s) {
  // this is an internal function only called after checking sample quality and on X
  if(s.sex == "female") {
    return s.affected == s.hom_alt;
  } else if (s.sex == "male") {
    if (s.affected && s.het && hom_ref_parent(s)) { return false; }
    return s.affected == (s.het || s.hom_alt);
  } else {
    return false;
  }
}

function segregating_recessive(s) {
  if(!hq1(s)){ return false; }
  if(variant.CHROM == "chrX" || variant.CHROM == "X") { return segregating_recessive_x(s); }
  if(s.affected){
    return s.hom_alt
  }
  return s.het || s.hom_ref
}

function parents_x_dn_or_homref(s) {
    if(!("mom" in s)) { return false; }
    if(!("dad" in s)) { return false; }
	return (hom_ref(s.mom) || (s.mom && segregating_denovo_x(s.mom)))
	    && (hom_ref(s.dad) || (s.dad && segregating_denovo_x(s.dad)))
}

// this function is used internally. called from segregating de novo.
// we already know it's on chrX
function segregating_denovo_x(s) {
  if(s.sex == "female") {
    // in this sample, the variant may not appear denovo, but we dont want to rule out a transmitted
    // de novo, so we check the parents of this sample.
    if(s.affected) { return s.het && hq1(s) && parents_x_dn_or_homref(s) }
    return s.hom_ref
  }
  if(s.sex == "male") {
    if(s.affected)  { return (s.het || s.hom_alt) && parents_x_dn_or_homref(s) }
    return s.hom_ref
  }
  return false
}

function affected_het_leaf(s) {
    // check if sample that is het has a parent who 
    // is also het without a parent
    if("mom" in s && !affected_het_leaf(s.mom)) { return false; }
    if("dad" in s && !affected_het_leaf(s.dad)) { return false; }
    return true;
}

function segregating_denovo(s) {
  if( !hq1(s)) { return false; }
 // if (variant.CHROM == "chrX" || variant.CHROM == "X") { return segregating_denovo_x(s); }
  if (!s.affected) { return s.hom_ref }
  if (s.hom_alt) { return false }
  if (!( s.het && s.AB >= config.min_AB && s.AB <= (1 - config.min_AB))) { return false; }
  // so far we just have segregating dominant. now have to check that somewhere
  // there's a mendelian violation
  return ("mom" in s) && ("dad" in s)
}