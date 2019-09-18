import os

def count(file):
    total = 0
    malware = 0
    for line in file:
        total += 1
        domain = line.split(' ')[1]
        if domain not in benighIP:
            malware +=1
    print(str(malware)+'/'+str(total))


baseDir = os.path.dirname(os.getcwd())
benighIP = ['time.windows.com', 'aeroinc.net', 'www.it885.com.cn', 'lrqxvrqsihwtudox.com',
            'eeuprbpohspwje.com', 'tlxfrilp.com', 'itehtxcch.com', 'snkbcptiqgqmlvw.com',
            'rykgnuncbedueeuevxg.com', 'absqvhpldvsmclt.com', 'view.atdmt.com', 'b.scorecardresearch.com',
            'ad.doubleclick.net', 'www.facebook.com', 'www.prettylikeher.com', 'www.google-analytics.com',
            'redirect.xmladfeed.com', 'connect.facebook.net', 'tags.bluekai.com', 'optimized-by.rubiconproject.com',
            'tap2-cdn.rubiconproject.com', 'ad.turn.com', 'map.media6degrees.com', 'bs.serving-sys.com', 'image2.pubmatic.com',
            'cm.g.doubleclick.net', 'r.openx.net', 'ce.lijit.com', 'i.w55c.net', 'adadvisor.net', 'd.p-td.com', 'ak1.abmr.net',
            'a.tribalfusion.com', 'user.lucidmedia.com', 'ib.mookie1.com', 'r.nexac.com', 'loadm.exelator.com', 'segment-pixel.invitemedia.com',
            'load.s3.amazonaws.com', 'ads.adxpose.com', 'cdn.fastclick.net', 'media.fastclick.net', 'event.adxpose.com', 'choices.truste.com', 'ads.revsci.net', 'ec.atdmt.com', 'bid.openx.net', 'www.googleadservices.com', 'googleads.g.doubleclick.net', 'search.yahoo.com', 'ads-vrx.httpads.com', 'www.lijit.com', 'um.simpli.fi', 'pagead2.googlesyndication.com', 'redir.adap.tv', 'apr.lijit.com', 'beacon.lijit.com', 'lj.d.chango.com', 'idpix.media6degrees.com', 'c.betrad.com', 'l.betrad.com', 'pix04.revsci.net', 'load.exelator.com', 'ad.z5x.net', 'search.spotxchange.com', 'cdn.doubleverify.com', 'fw.adsafeprotected.com', 'tags.expo9.exponential.com', 'secure-us.imrworldwide.com', 'cp79082.edgefcs.net', 'ocsp.verisign.com', 'lixht.gnway.net', 'netuser.dns1.us', 'comcast.netil.com', 'imperatively.com', 'hoymail.com', 'patmedia.net', 'cotv.net', 'scrupulously.com', 'aaol.com', 'aoil.com', 'peppiness.com', 'complete1.com', '2onesource.com', 'stepan.cails.com', 'chsmail.org', 'raygroup.com', 'mountaincable.net', 'benchcraft.com', 'haphazardness.com', 'carolinarr.com', 'ipro.net', 'pendragonstaffing.com', 'chestertel.com', 'tunefulness.com', 'marginalization.com', 'creepily.com', 'bellsout.net', 'entertainmentresource.com', 'aol.coml.com', 'eartlink.net', 'erimail.com', 'canada.com', 'optline.net', 'royalgardens.com', 'sabinenet.com', 'electriciti.com', 'alloymail.com', 'neenahprinting.com', 'groups.msn.com', 'sunterra.com', 'gotmail.com', 'sbcglobalnet.com', 'medscape.com', 'alanticbb.net', '1.courier-push-apple.com.akadns.net', 'yahoo.com', 'gmail.com']




with open(os.path.join(baseDir, 'processedData', 'final_result_withoutpattern.txt')) as fSuffix:
    with open(os.path.join(baseDir, 'processedData', 'WARP_result.txt')) as fWARP:
        with open(os.path.join(baseDir, 'processedData', 'Autocorrelation_result.txt')) as fcorrelation:
            with open(os.path.join(baseDir, 'processedData', 'conv_segmentDetection.txt')) as fConv_seg:
                with open(os.path.join(baseDir, 'processedData', 'conv_symbolDetection.txt')) as fConv_Symbol:
                    with open(os.path.join(baseDir, 'processedData', 'FFT_final.txt')) as fFFT:
                        file_dict={"Suffix":fSuffix,"WARP":fWARP,"AutoCorrelation":fcorrelation,"Conv_seg":fConv_seg,"Conv_Symbol":fConv_Symbol,"FFT":fFFT}
                        for key,value in file_dict.items():
                            print(key)
                            count(value)
                            print('----------------------------')