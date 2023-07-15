#![allow(non_snake_case)]
use std::collections::HashMap;
use lazy_static::lazy_static;


lazy_static! {

	pub static ref sBox: HashMap<(&'static str, &'static str), &'static str> = {

		let mut aes = HashMap::new();
		aes.extend([(("00", "00"), "63"), (("00", "01"), "7c"), (("00", "02"), "77"), (("00", "03"), "7b"), (("00", "04"), "f2"), (("00", "05"), "6b"), (("00", "06"), "6f"), (("00", "07"), "c5"), (("00", "08"), "30"), (("00", "09"), "01"), (("00", "0a"), "67"), (("00", "0b"), "2b"), (("00", "0c"), "fe"), (("00", "0d"), "d7"), (("00", "0e"), "ab"), (("00", "0f"), "76"),
					(("10", "00"), "ca"), (("10", "01"), "82"), (("10", "02"), "c9"), (("10", "03"), "7d"), (("10", "04"), "fa"), (("10", "05"), "59"), (("10", "06"), "47"), (("10", "07"), "f0"), (("10", "08"), "ad"), (("10", "09"), "d4"), (("10", "0a"), "a2"), (("10", "0b"), "af"), (("10", "0c"), "9c"), (("10", "0d"), "a4"), (("10", "0e"), "72"), (("10", "0f"), "c0"),
					(("20", "00"), "b7"), (("20", "01"), "fd"), (("20", "02"), "93"), (("20", "03"), "26"), (("20", "04"), "36"), (("20", "05"), "3f"), (("20", "06"), "f7"), (("20", "07"), "cc"), (("20", "08"), "34"), (("20", "09"), "a5"), (("20", "0a"), "e5"), (("20", "0b"), "f1"), (("20", "0c"), "71"), (("20", "0d"), "d8"), (("20", "0e"), "31"), (("20", "0f"), "15"),
					(("30", "00"), "04"), (("30", "01"), "c7"), (("30", "02"), "23"), (("30", "03"), "c3"), (("30", "04"), "18"), (("30", "05"), "96"), (("30", "06"), "05"), (("30", "07"), "9a"), (("30", "08"), "07"), (("30", "09"), "12"), (("30", "0a"), "80"), (("30", "0b"), "e2"), (("30", "0c"), "eb"), (("30", "0d"), "27"), (("30", "0e"), "b2"), (("30", "0f"), "75"),
					(("40", "00"), "09"), (("40", "01"), "83"), (("40", "02"), "2c"), (("40", "03"), "1a"), (("40", "04"), "1b"), (("40", "05"), "6e"), (("40", "06"), "5a"), (("40", "07"), "a0"), (("40", "08"), "52"), (("40", "09"), "3b"), (("40", "0a"), "d6"), (("40", "0b"), "b3"), (("40", "0c"), "29"), (("40", "0d"), "e3"), (("40", "0e"), "2f"), (("40", "0f"), "84"),
					(("50", "00"), "53"), (("50", "01"), "d1"), (("50", "02"), "00"), (("50", "03"), "ed"), (("50", "04"), "20"), (("50", "05"), "fc"), (("50", "06"), "b1"), (("50", "07"), "5b"), (("50", "08"), "6a"), (("50", "09"), "cb"), (("50", "0a"), "be"), (("50", "0b"), "39"), (("50", "0c"), "4a"), (("50", "0d"), "4c"), (("50", "0e"), "58"), (("50", "0f"), "cf"),
					(("60", "00"), "d0"), (("60", "01"), "ef"), (("60", "02"), "aa"), (("60", "03"), "fb"), (("60", "04"), "43"), (("60", "05"), "4d"), (("60", "06"), "33"), (("60", "07"), "85"), (("60", "08"), "45"), (("60", "09"), "f9"), (("60", "0a"), "02"), (("60", "0b"), "7f"), (("60", "0c"), "50"), (("60", "0d"), "3c"), (("60", "0e"), "9f"), (("60", "0f"), "a8"),
					(("70", "00"), "51"), (("70", "01"), "a3"), (("70", "02"), "40"), (("70", "03"), "8f"), (("70", "04"), "92"), (("70", "05"), "9d"), (("70", "06"), "38"), (("70", "07"), "f5"), (("70", "08"), "bc"), (("70", "09"), "b6"), (("70", "0a"), "da"), (("70", "0b"), "21"), (("70", "0c"), "10"), (("70", "0d"), "ff"), (("70", "0e"), "f3"), (("70", "0f"), "d2"),
					(("80", "00"), "cd"), (("80", "01"), "0c"), (("80", "02"), "13"), (("80", "03"), "ec"), (("80", "04"), "5f"), (("80", "05"), "97"), (("80", "06"), "44"), (("80", "07"), "17"), (("80", "08"), "c4"), (("80", "09"), "a7"), (("80", "0a"), "7e"), (("80", "0b"), "3d"), (("80", "0c"), "64"), (("80", "0d"), "5d"), (("80", "0e"), "19"), (("80", "0f"), "73"),
					(("90", "00"), "60"), (("90", "01"), "81"), (("90", "02"), "4f"), (("90", "03"), "dc"), (("90", "04"), "22"), (("90", "05"), "2a"), (("90", "06"), "90"), (("90", "07"), "88"), (("90", "08"), "46"), (("90", "09"), "ee"), (("90", "0a"), "b8"), (("90", "0b"), "14"), (("90", "0c"), "de"), (("90", "0d"), "5e"), (("90", "0e"), "0b"), (("90", "0f"), "db"),
					(("a0", "00"), "e0"), (("a0", "01"), "32"), (("a0", "02"), "3a"), (("a0", "03"), "0a"), (("a0", "04"), "49"), (("a0", "05"), "06"), (("a0", "06"), "24"), (("a0", "07"), "5c"), (("a0", "08"), "c2"), (("a0", "09"), "d3"), (("a0", "0a"), "ac"), (("a0", "0b"), "62"), (("a0", "0c"), "91"), (("a0", "0d"), "95"), (("a0", "0e"), "e4"), (("a0", "0f"), "79"),
					(("b0", "00"), "e7"), (("b0", "01"), "c8"), (("b0", "02"), "37"), (("b0", "03"), "6d"), (("b0", "04"), "8d"), (("b0", "05"), "d5"), (("b0", "06"), "4e"), (("b0", "07"), "a9"), (("b0", "08"), "6c"), (("b0", "09"), "56"), (("b0", "0a"), "f4"), (("b0", "0b"), "ea"), (("b0", "0c"), "65"), (("b0", "0d"), "7a"), (("b0", "0e"), "ae"), (("b0", "0f"), "08"),
					(("c0", "00"), "ba"), (("c0", "01"), "78"), (("c0", "02"), "25"), (("c0", "03"), "2e"), (("c0", "04"), "1c"), (("c0", "05"), "a6"), (("c0", "06"), "b4"), (("c0", "07"), "c6"), (("c0", "08"), "e8"), (("c0", "09"), "dd"), (("c0", "0a"), "74"), (("c0", "0b"), "1f"), (("c0", "0c"), "4b"), (("c0", "0d"), "bd"), (("c0", "0e"), "8b"), (("c0", "0f"), "8a"),
					(("d0", "00"), "70"), (("d0", "01"), "3e"), (("d0", "02"), "b5"), (("d0", "03"), "66"), (("d0", "04"), "48"), (("d0", "05"), "03"), (("d0", "06"), "f6"), (("d0", "07"), "0e"), (("d0", "08"), "61"), (("d0", "09"), "35"), (("d0", "0a"), "57"), (("d0", "0b"), "b9"), (("d0", "0c"), "86"), (("d0", "0d"), "c1"), (("d0", "0e"), "1d"), (("d0", "0f"), "9e"),
					(("e0", "00"), "e1"), (("e0", "01"), "f8"), (("e0", "02"), "98"), (("e0", "03"), "11"), (("e0", "04"), "69"), (("e0", "05"), "d9"), (("e0", "06"), "8e"), (("e0", "07"), "94"), (("e0", "08"), "9b"), (("e0", "09"), "1e"), (("e0", "0a"), "87"), (("e0", "0b"), "e9"), (("e0", "0c"), "ce"), (("e0", "0d"), "55"), (("e0", "0e"), "28"), (("e0", "0f"), "df"),
					(("f0", "00"), "8c"), (("f0", "01"), "a1"), (("f0", "02"), "89"), (("f0", "03"), "0d"), (("f0", "04"), "bf"), (("f0", "05"), "e6"), (("f0", "06"), "42"), (("f0", "07"), "68"), (("f0", "08"), "41"), (("f0", "09"), "99"), (("f0", "0a"), "2d"), (("f0", "0b"), "0f"), (("f0", "0c"), "b0"), (("f0", "0d"), "54"), (("f0", "0e"), "bb"), (("f0", "0f"), "16")].iter().cloned());

		aes

    };

}

lazy_static! {

	pub static ref inverseSubstitution: HashMap<(&'static str, &'static str), &'static str> = {

		let mut aes = HashMap::new();
		aes.extend([(("00", "00"), "52"), (("00", "01"), "09"), (("00", "02"), "6a"), (("00", "03"), "d5"), (("00", "04"), "30"), (("00", "05"), "36"), (("00", "06"), "a5"), (("00", "07"), "38"), (("00", "08"), "bf"), (("00", "09"), "40"), (("00", "0a"), "a3"), (("00", "0b"), "9e"), (("00", "0c"), "81"), (("00", "0d"), "f3"), (("00", "0e"), "d7"), (("00", "0f"), "fb"),
					(("10", "00"), "7c"), (("10", "01"), "e3"), (("10", "02"), "39"), (("10", "03"), "82"), (("10", "04"), "9b"), (("10", "05"), "2f"), (("10", "06"), "ff"), (("10", "07"), "87"), (("10", "08"), "34"), (("10", "09"), "8e"), (("10", "0a"), "43"), (("10", "0b"), "44"), (("10", "0c"), "c4"), (("10", "0d"), "de"), (("10", "0e"), "e9"), (("10", "0f"), "cb"),
					(("20", "00"), "54"), (("20", "01"), "7b"), (("20", "02"), "94"), (("20", "03"), "32"), (("20", "04"), "a6"), (("20", "05"), "c2"), (("20", "06"), "23"), (("20", "07"), "3d"), (("20", "08"), "ee"), (("20", "09"), "4c"), (("20", "0a"), "95"), (("20", "0b"), "0b"), (("20", "0c"), "42"), (("20", "0d"), "fa"), (("20", "0e"), "c3"), (("20", "0f"), "4e"),
					(("30", "00"), "08"), (("30", "01"), "2e"), (("30", "02"), "a1"), (("30", "03"), "66"), (("30", "04"), "28"), (("30", "05"), "d9"), (("30", "06"), "24"), (("30", "07"), "b2"), (("30", "08"), "76"), (("30", "09"), "5b"), (("30", "0a"), "a2"), (("30", "0b"), "49"), (("30", "0c"), "6d"), (("30", "0d"), "8b"), (("30", "0e"), "d1"), (("30", "0f"), "25"),
					(("40", "00"), "72"), (("40", "01"), "f8"), (("40", "02"), "f6"), (("40", "03"), "64"), (("40", "04"), "86"), (("40", "05"), "68"), (("40", "06"), "98"), (("40", "07"), "16"), (("40", "08"), "d4"), (("40", "09"), "a4"), (("40", "0a"), "5c"), (("40", "0b"), "cc"), (("40", "0c"), "5d"), (("40", "0d"), "65"), (("40", "0e"), "b6"), (("40", "0f"), "92"),
					(("50", "00"), "6c"), (("50", "01"), "70"), (("50", "02"), "48"), (("50", "03"), "50"), (("50", "04"), "fd"), (("50", "05"), "ed"), (("50", "06"), "b9"), (("50", "07"), "da"), (("50", "08"), "5e"), (("50", "09"), "15"), (("50", "0a"), "46"), (("50", "0b"), "57"), (("50", "0c"), "a7"), (("50", "0d"), "8d"), (("50", "0e"), "9d"), (("50", "0f"), "84"),
					(("60", "00"), "90"), (("60", "01"), "d8"), (("60", "02"), "ab"), (("60", "03"), "00"), (("60", "04"), "8c"), (("60", "05"), "bc"), (("60", "06"), "d3"), (("60", "07"), "0a"), (("60", "08"), "f7"), (("60", "09"), "e4"), (("60", "0a"), "58"), (("60", "0b"), "05"), (("60", "0c"), "b8"), (("60", "0d"), "b3"), (("60", "0e"), "45"), (("60", "0f"), "06"),
					(("70", "00"), "d0"), (("70", "01"), "2c"), (("70", "02"), "1e"), (("70", "03"), "8f"), (("70", "04"), "ca"), (("70", "05"), "3f"), (("70", "06"), "0f"), (("70", "07"), "02"), (("70", "08"), "c1"), (("70", "09"), "af"), (("70", "0a"), "bd"), (("70", "0b"), "03"), (("70", "0c"), "01"), (("70", "0d"), "13"), (("70", "0e"), "8a"), (("70", "0f"), "6b"),
					(("80", "00"), "3a"), (("80", "01"), "91"), (("80", "02"), "11"), (("80", "03"), "41"), (("80", "04"), "4f"), (("80", "05"), "67"), (("80", "06"), "dc"), (("80", "07"), "ea"), (("80", "08"), "97"), (("80", "09"), "f2"), (("80", "0a"), "cf"), (("80", "0b"), "ce"), (("80", "0c"), "f0"), (("80", "0d"), "b4"), (("80", "0e"), "e6"), (("80", "0f"), "73"),
					(("90", "00"), "96"), (("90", "01"), "ac"), (("90", "02"), "74"), (("90", "03"), "22"), (("90", "04"), "e7"), (("90", "05"), "ad"), (("90", "06"), "35"), (("90", "07"), "85"), (("90", "08"), "e2"), (("90", "09"), "f9"), (("90", "0a"), "37"), (("90", "0b"), "e8"), (("90", "0c"), "1c"), (("90", "0d"), "75"), (("90", "0e"), "df"), (("90", "0f"), "6e"),
					(("a0", "00"), "47"), (("a0", "01"), "f1"), (("a0", "02"), "1a"), (("a0", "03"), "71"), (("a0", "04"), "1d"), (("a0", "05"), "29"), (("a0", "06"), "c5"), (("a0", "07"), "89"), (("a0", "08"), "6f"), (("a0", "09"), "b7"), (("a0", "0a"), "62"), (("a0", "0b"), "0e"), (("a0", "0c"), "aa"), (("a0", "0d"), "18"), (("a0", "0e"), "be"), (("a0", "0f"), "1b"),
					(("b0", "00"), "fc"), (("b0", "01"), "56"), (("b0", "02"), "3e"), (("b0", "03"), "4b"), (("b0", "04"), "c6"), (("b0", "05"), "d2"), (("b0", "06"), "79"), (("b0", "07"), "20"), (("b0", "08"), "9a"), (("b0", "09"), "db"), (("b0", "0a"), "c0"), (("b0", "0b"), "fe"), (("b0", "0c"), "78"), (("b0", "0d"), "cd"), (("b0", "0e"), "5a"), (("b0", "0f"), "f4"),
					(("c0", "00"), "1f"), (("c0", "01"), "dd"), (("c0", "02"), "a8"), (("c0", "03"), "33"), (("c0", "04"), "88"), (("c0", "05"), "07"), (("c0", "06"), "c7"), (("c0", "07"), "31"), (("c0", "08"), "b1"), (("c0", "09"), "12"), (("c0", "0a"), "10"), (("c0", "0b"), "59"), (("c0", "0c"), "27"), (("c0", "0d"), "80"), (("c0", "0e"), "ec"), (("c0", "0f"), "5f"),
					(("d0", "00"), "60"), (("d0", "01"), "51"), (("d0", "02"), "7f"), (("d0", "03"), "a9"), (("d0", "04"), "19"), (("d0", "05"), "b5"), (("d0", "06"), "4a"), (("d0", "07"), "0d"), (("d0", "08"), "2d"), (("d0", "09"), "e5"), (("d0", "0a"), "7a"), (("d0", "0b"), "9f"), (("d0", "0c"), "93"), (("d0", "0d"), "c9"), (("d0", "0e"), "9c"), (("d0", "0f"), "ef"),
					(("e0", "00"), "a0"), (("e0", "01"), "e0"), (("e0", "02"), "3b"), (("e0", "03"), "4d"), (("e0", "04"), "ae"), (("e0", "05"), "2a"), (("e0", "06"), "f5"), (("e0", "07"), "b0"), (("e0", "08"), "c8"), (("e0", "09"), "eb"), (("e0", "0a"), "bb"), (("e0", "0b"), "3c"), (("e0", "0c"), "83"), (("e0", "0d"), "53"), (("e0", "0e"), "99"), (("e0", "0f"), "61"),
					(("f0", "00"), "17"), (("f0", "01"), "2b"), (("f0", "02"), "04"), (("f0", "03"), "7e"), (("f0", "04"), "ba"), (("f0", "05"), "77"), (("f0", "06"), "d6"), (("f0", "07"), "26"), (("f0", "08"), "e1"), (("f0", "09"), "69"), (("f0", "0a"), "14"), (("f0", "0b"), "63"), (("f0", "0c"), "55"), (("f0", "0d"), "21"), (("f0", "0e"), "0c"), (("f0", "0f"), "7d")].iter().cloned());

		aes

	};

}

lazy_static! {

	pub static ref roundConstants: HashMap<i8, Vec<&'static str>> = {

		let mut table = HashMap::new();
		table.insert(1, vec!["01", "00", "00", "00"]);
		table.insert(2, vec!["02", "00", "00", "00"]);
		table.insert(3, vec!["04", "00", "00", "00"]);
		table.insert(4, vec!["08", "00", "00", "00"]);
		table.insert(5, vec!["10", "00", "00", "00"]);
		table.insert(6, vec!["20", "00", "00", "00"]);
		table.insert(7, vec!["40", "00", "00", "00"]);
		table.insert(8, vec!["80", "00", "00", "00"]);
		table.insert(9, vec!["1b", "00", "00", "00"]);
		table.insert(10, vec!["36", "00", "00", "00"]);
		table.insert(11, vec!["6c", "00", "00", "00"]);
		table.insert(12, vec!["d8", "00", "00", "00"]);
		table.insert(13, vec!["ab", "00", "00", "00"]);
		table.insert(14, vec!["4d", "00", "00", "00"]);
		table

	};

}
// let hex_string = hex.to_owned();
// let decimal = u8::from_str_radix(&hex_string, 16).unwrap();
