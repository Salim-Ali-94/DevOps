#![allow(non_snake_case)]
use rand::Rng;


pub fn aesKeyGenerator(mut key_length: i16) -> (String, Vec<String>, i8) {

	let mut rng = rand::thread_rng();
	let mut key = if rng.gen_range(0.0..1.0) < 0.5 { "1".to_owned() } else { "0".to_string() };
	let rounds;

	if key_length <= 128 {

		key_length = 128;
		rounds = 10;

	} else if key_length > 128 && key_length <= 192 {

		key_length = 192;
		rounds = 12;

	} else {

		key_length = 256;
		rounds = 14;

	}

	while key.len() < key_length as usize {

        if rng.gen_range(0.0..1.0) < 0.5 {

            key.push_str("1");

        } else {

            key.push_str("0");

        }
        
	}

	key = shuffleBits(key);
	let hex = partitionBits(key.clone(), (key_length / 16).try_into().unwrap());
	return (key, hex, rounds);

}

fn shuffleBits(bits: String) -> String {

	let mut rng = rand::thread_rng();
	let mut word = String::from(&bits);
	let mut address_a;
	let mut address_b;
	let mut bit_a;
	let mut bit_b;

	for _ in 0..bits.len() {

		address_a = rng.gen_range(0..bits.len());
		bit_a = word.chars().nth(address_a).unwrap();
		address_b = rng.gen_range(0..bits.len());
		bit_b = word.chars().nth(address_b).unwrap();

		while bit_b == bit_a || address_b == address_a {

			address_b = rng.gen_range(0..bits.len());
			bit_b = word.chars().nth(address_b).unwrap();

		}

		word.replace_range(address_a..address_a + 1, &bit_b.to_string());
		word.replace_range(address_b..address_b + 1, &bit_a.to_string());

	}

	return word;

}

fn partitionBits(bits: String, block: i8) -> Vec<String> {

	let mut sections = vec![];

	for word in (0..bits.len()).step_by(block as usize) {

		sections.push(format!("{:0width$x}",
							  u32::from_str_radix(&bits[word..word + block as usize], 2).unwrap(),
							  width = block as usize / 4));

	}

	return sections;

}
