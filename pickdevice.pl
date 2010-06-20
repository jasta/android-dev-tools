#!/usr/bin/env perl
###############################################################################
##
## Easily manipulate the value of ANDROID_SERIAL by presenting an interactive
## list of currently connected devices. 
##
## Designed to be invoked by the shell as:
##
##   eval $(pickdevice)
##
###############################################################################

use strict;
use Data::Dumper;

###############################################################################

my @devicesOutput = qx{adb devices};
shift(@devicesOutput) =~ m/^List of devices/i or
		die "Unexpected `adb devices' output.\n";

my @devices;
my $defaultChoice;

foreach (@devicesOutput) {
	chomp;
	next if m/^\s*$/;

	my ($serial, $desc) = split /\s+/, $_, 2;

	push @devices, { serial => $serial, desc => $desc };

	if (!defined($defaultChoice) && $serial !~ m/^emulator/) {
		$defaultChoice = $#devices;
	}
}

if (@devices == 0) {
	die "No devices connected?\n";
}

if (!defined($defaultChoice)) {
	$defaultChoice = 0;
}

print STDERR "Pick a device:\n";

for (0 .. $#devices) {
	print STDERR "\t", $_, ". ", $devices[$_]->{serial}, "\n";
}

print STDERR "\n";
print STDERR "Which would you like for ANDROID_SERIAL? [$defaultChoice] ";
chomp (my $answer = <STDIN>);

if (length $answer == 0) {
	$answer = $defaultChoice;
}

print "export ANDROID_SERIAL=", $devices[$answer]->{serial}, "\n";
