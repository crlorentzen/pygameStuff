#!/bin/bash
SCRIPT=$1
/usr/bin/env python $SCRIPT
RETVAL=$?
while [ $RETVAL == 0 ]; do
	/usr/bin/env python $SCRIPT
	RETVAL=$?
done
