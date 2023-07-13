#![allow(non_snake_case)]
use std::collections::HashMap;


pub fn sBox<'a>(row: &'a str, column: &'a str) -> &'a str {

	let aes_substitution = HashMap::from([(("00", "00"), "63"), (("00", "01"), "7c"), (("00", "02"), "77"), (("00", "03"), "7b"), (("00", "04"), "f2"), (("00", "05"), "6b"), (("00", "06"), "6f"), (("00", "07"), "c5"), (("00", "08"), "30"), (("00", "09"), "01"), (("00", "0a"), "67"), (("00", "0b"), "2b"), (("00", "0c"), "fe"), (("00", "0d"), "d7"), (("00", "0e"), "ab"), (("00", "0f"), "76"),
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
										  (("f0", "00"), "8c"), (("f0", "01"), "a1"), (("f0", "02"), "89"), (("f0", "03"), "0d"), (("f0", "04"), "bf"), (("f0", "05"), "e6"), (("f0", "06"), "42"), (("f0", "07"), "68"), (("f0", "08"), "41"), (("f0", "09"), "99"), (("f0", "0a"), "2d"), (("f0", "0b"), "0f"), (("f0", "0c"), "b0"), (("f0", "0d"), "54"), (("f0", "0e"), "bb"), (("f0", "0f"), "16")]);

	return aes_substitution.get(&(row, column)).unwrap();

}

// 	00	01	02	03	04	05	06	07	08	09	0a	0b	0c	0d	0e	0f
// 00	52	09	6a	d5	30	36	a5	38	bf	40	a3	9e	81	f3	d7	fb
// 10	7c	e3	39	82	9b	2f	ff	87	34	8e	43	44	c4	de	e9	cb
// 20	54	7b	94	32	a6	c2	23	3d	ee	4c	95	0b	42	fa	c3	4e
// 30	08	2e	a1	66	28	d9	24	b2	76	5b	a2	49	6d	8b	d1	25
// 40	72	f8	f6	64	86	68	98	16	d4	a4	5c	cc	5d	65	b6	92
// 50	6c	70	48	50	fd	ed	b9	da	5e	15	46	57	a7	8d	9d	84
// 60	90	d8	ab	00	8c	bc	d3	0a	f7	e4	58	05	b8	b3	45	06
// 70	d0	2c	1e	8f	ca	3f	0f	02	c1	af	bd	03	01	13	8a	6b
// 80	3a	91	11	41	4f	67	dc	ea	97	f2	cf	ce	f0	b4	e6	73
// 90	96	ac	74	22	e7	ad	35	85	e2	f9	37	e8	1c	75	df	6e
// a0	47	f1	1a	71	1d	29	c5	89	6f	b7	62	0e	aa	18	be	1b
// b0	fc	56	3e	4b	c6	d2	79	20	9a	db	c0	fe	78	cd	5a	f4
// c0	1f	dd	a8	33	88	07	c7	31	b1	12	10	59	27	80	ec	5f
// d0	60	51	7f	a9	19	b5	4a	0d	2d	e5	7a	9f	93	c9	9c	ef
// e0	a0	e0	3b	4d	ae	2a	f5	b0	c8	eb	bb	3c	83	53	99	61
// f0	17	2b	04	7e	ba	77	d6	26	e1	69	14	63	55	21	0c	7d