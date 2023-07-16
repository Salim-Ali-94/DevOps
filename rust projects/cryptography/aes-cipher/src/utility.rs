#![allow(non_snake_case)]
use rand::Rng;
pub mod constants;


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
	let hex = partitionBits(key.clone());
	return (key, hex, rounds);

}

pub fn shuffleBits(bits: String) -> String {

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

pub fn partitionBits(bits: String) -> Vec<String> {

	let mut sections = vec![];

	for byte in (0..bits.len()).step_by(8) {

		sections.push(format!("{:0width$x}",
							  u32::from_str_radix(&bits[byte..byte + 8], 2).unwrap(),
							  width = 2));

	}

	return sections;

}

pub fn stackBytes(blocks: Vec<String>) -> Vec<Vec<String>> {

	let mut matrix = vec![];

	for block in blocks.chunks(4) {

		matrix.push(block.to_vec());

	}

	return matrix;

}

pub fn encodeDocument(message: String) -> (String, String) {

	let mut binary = String::new();
	let mut hex = String::new();

	for character in message.chars() {

		binary.push_str(&format!("{:08b}", character as u8));
		hex.push_str(&format!("{:02x}", character as u32));

	}

	return (binary, hex);

}

pub fn partitionDocument(mut message: String, chunk: i16) -> Vec<Vec<Vec<String>>> {

	let mut document = vec![];
	let mut buffer = vec![];
	let mut column = vec![];
	let mut block;

	while message.len() % chunk as usize != 0 {

		message.push_str(&format!("{:08b}", b'~'));

	}

	for word in (0..message.len()).step_by(chunk as usize) {

		block = message[word..word + chunk as usize].to_string();

		for character in (0..chunk as usize).step_by(8) {

			column.push(block[character..character + 8].to_string());

			if column.len() == 4 {

				buffer.push(column.clone());
				column.clear();

			}

		}

		document.push(buffer.clone());
		buffer.clear();

	}

	return document;

}

pub fn partitionMessage(mut message: String, chunk: i16) -> Vec<Vec<Vec<String>>> {

	let mut document = vec![];
	let mut buffer = vec![];
	let mut column = vec![];
	let mut block;

	while message.len() % (chunk as usize) / 4 != 0 {

		message.push_str(&format!("{:02x}", b'~'));

	}

	for word in (0..message.len()).step_by((chunk as usize) / 4) {

		block = message[word..word + (chunk as usize) / 4].to_string();

		for character in (0..(chunk as usize) / 4).step_by(8 / 4) {
		
			column.push(block[character..character + 8 / 4].to_string());

			if column.len() == 4 {

				buffer.push(column.clone());
				column.clear();

			}

		}

		document.push(buffer.clone());
		buffer.clear();

	}

	return document;

}

pub fn shuffleVector(mut word: Vec<String>) -> Vec<String> {

	let constant = constants::roundConstants.get(&2).unwrap();
	word = leftShift(word);
	word = forwardSubstitution(word);
	word = xor(word, constant.clone());
	return word;

}

pub fn leftShift(mut word: Vec<String>) -> Vec<String> {

	let buffer = word.remove(0);
	word.push(buffer);
	return word;

}

pub fn formatIndex(character: String) -> (String, String) {

	let mut row = character.chars().nth(0).unwrap().to_string();
	let mut column = character.chars().nth(1).unwrap().to_string();
	row.push_str("0");
	column = "0".to_owned() + &column;
	return (row, column);

}

pub fn forwardSubstitution(mut word: Vec<String>) -> Vec<String> {

	for character in word.iter_mut() {

		let (row, column) = formatIndex(character.clone());
		*character = constants::sBox.get(&(&row, &column)).unwrap().to_string();

	}

	return word;

}

pub fn xor(mut word: Vec<String>, constant: Vec<&str>) -> Vec<String> {

	let binary = u8::from_str_radix(&word[0], 16).unwrap();
	let vector = u8::from_str_radix(&constant[0], 16).unwrap();
	let sum = binary ^ vector;
	word[0] = format!("{:02x}", sum);
	return word;

}


// pub fn XOR(mut word: Vec<String>, constant: Vec<&str>) -> Vec<String> {

// 	for (index, character) in word.iter_mut().enumerate() {

// 		let binary = u8::from_str_radix(&character, 16).unwrap();
// 		let vector = u8::from_str_radix(&constant[index], 16).unwrap();
// 		let sum = binary ^ vector;
// 		*character = format!("{:02x}", sum);

// 	}

// 	return word;

// }

// pub fn encryptDocument(document: Vec<Vec<String>>) -> String {

// 	return "document";

// }
