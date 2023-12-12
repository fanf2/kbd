#!/usr/bin/perl

use warnings;
use strict;

my $sw_ref;
my $d_ref;

while (<>) {
	if (m{property "Reference" "SW\d+" \(at ([0-9.]+) ([0-9.]+) }) {
		my $col = int($1 / 14) - 1;
		my $y = int($2 / 13) + 2;
		my $row = int($y / 3);
		my $sub = $row == 5 ? 0 : ($y % 3) + 1;
		$sw_ref = "SW$row$sub$col";
	}
	if (m{property "Reference" "D\d+" \(at ([0-9.]+) ([0-9.]+) }) {
		my $col = int($1 / 14) - 1;
		my $y = int($2 / 13) + 2;
		my $row = int($y / 3);
		my $sub = $row == 5 ? 0 : ($y % 3) + 1;
		$d_ref = "D$row$sub$col";
	}
	$_ =~ s{"SW\d+"}{"$sw_ref"};
	$_ =~ s{"D\d+"}{"$d_ref"};
	print;
}
