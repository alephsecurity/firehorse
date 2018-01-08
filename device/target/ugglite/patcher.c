/*
firehorse
by Roee Hay & Noam Hadad, Aleph Research
*/

#include "../../fh.h"

STACKHOOK(fhpatcher)
{
    DD("Firehose patcher called!");
    
    init();

    DD("Firehose patcher done!");}


STACKHOOK(pblpatcher)
{
    DD("Hello from PBL patcher");
    fh_dacr();
    pagecopy();
    pageremap();
    init();

    DD("Good bye from PBL patcher");
    
}

void cb_patchtz(cbargs *args)
{
}
void cb_sblpatcher(cbargs *args)
{


}
void cb_ablpatcher(cbargs *args)
{

    
}

void cb_before_linux()
{

}

void cb_mmcread()
{

}

void cb_bootlinux(cbargs *cb)
{


}
