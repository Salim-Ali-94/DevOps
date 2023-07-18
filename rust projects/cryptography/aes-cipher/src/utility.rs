#![allow(non_snake_case)]
#![allow(clippy::needless_return)]
#![allow(clippy::type_complexity)]
use rand::Rng;
pub mod constants;


pub fn scrambleDocument(file: String, aes_standard: u16) -> (String, String, Vec<Vec<Vec<String>>>, Vec<Vec<String>>) {

    let (binary_key, key, rounds) = aesKeyGenerator(aes_standard);
    let (_, mut document) = spliceDocument(file.clone(), binary_key.len().try_into().unwrap());
	let mut lock = key.clone();
	let mut memory = vec![];

	for (index, block) in document.iter_mut().enumerate() {

		*block = XOR(block.to_vec(), key.clone());

		for round in 1..=rounds {

			if index == 0 {

				lock = scheduleKey(lock, round);
				memory.push(lock.clone());


			} else {

				lock = memory[round as usize].clone();

			}

			*block = sTransform(block.to_vec());
			*block = shiftRows(block.to_vec());

			if round != rounds - 1 {

				*block = mixColumns(block.to_vec());

			}

			*block = XOR(block.to_vec(), lock.clone());

		}

	}

	let cipher = collapseMatrix(document.clone());
	return (cipher, binary_key, document, key);

}

fn aesKeyGenerator(aes_standard: u16) -> (String, Vec<Vec<String>>, u8) {

	let mut rng = rand::thread_rng();
	let mut key = if rng.gen_range(0.0..1.0) < 0.5 { "1".to_owned() } else { "0".to_string() };
	let rounds;
	let key_length;

	if aes_standard <= 128 {

		key_length = 128;
		rounds = 10;

	} else if aes_standard > 128 && aes_standard <= 192 {

		key_length = 192;
		rounds = 12;

	} else {

		key_length = 256;
		rounds = 14;

	}

	while key.len() < key_length as usize {

        if rng.gen_range(0.0..1.0) < 0.5 {

            key.push('1');

        } else {

            key.push('0');

        }
        
	}

	key = shuffleBits(key);
	let hex = stackBytes(key.clone());
	return (key, hex, rounds);

}

fn spliceDocument(file: String, chunk: u16) -> (String, Vec<Vec<Vec<String>>>) {

	let mut message = encodeMessage(file);
	let mut document = vec![];
	let mut buffer = vec![];
	let mut column = vec![];
	let mut block;

	while message.len() % (chunk as usize / 4) != 0 {

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

	return (message, document);

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

fn partitionBits(bits: String) -> Vec<String> {

	let mut sections = vec![];

	for byte in (0..bits.len()).step_by(8) {

		sections.push(format!("{:02x}", u8::from_str_radix(&bits[byte..byte + 8], 2).unwrap()));

	}

	return sections;

}

fn stackBytes(bits: String) -> Vec<Vec<String>> {

	let blocks = partitionBits(bits);
	let mut matrix = vec![];

	for block in blocks.chunks(4) {

		matrix.push(block.to_vec());

	}

	return matrix;

}

fn encodeMessage(message: String) -> String {

	let mut hex = String::new();

	for character in message.chars() {

		hex.push_str(&format!("{:02x}", character as u32));

	}

	return hex;

}

fn shuffleVector(mut word: Vec<String>, round: u8) -> Vec<String> {

	let constant = constants::roundConstants.get(&round).unwrap();
	word = leftShift(word);
	word = forwardSubstitution(word);
	word[0] = xor(word[0].to_string(), constant.clone()[0].to_string());
	return word;

}

fn leftShift(mut word: Vec<String>) -> Vec<String> {

	let buffer = word.remove(0);
	word.push(buffer);
	return word;

}

fn formatIndex(character: String) -> (String, String) {

	let mut row = character.chars().next().unwrap().to_string();
	let mut column = character.chars().nth(1).unwrap().to_string();
	row.push('0');
	column = "0".to_owned() + &column;
	return (row, column);

}

fn forwardSubstitution(mut word: Vec<String>) -> Vec<String> {

	for character in word.iter_mut() {

		let (row, column) = formatIndex(character.clone());
		*character = constants::sBox.get(&(&row, &column)).unwrap().to_string();

	}

	return word;

}

fn xor(a: String, b: String) -> String {

	let x = u8::from_str_radix(&a, 16).unwrap();
	let y = u8::from_str_radix(&b, 16).unwrap();
	let sum = x ^ y;
	let c = format!("{:02x}", sum);
	return c;

}

fn XOR(mut data: Vec<Vec<String>>, matrix: Vec<Vec<String>>) -> Vec<Vec<String>> {

	for (row, array) in data.iter_mut().enumerate() {

		for (column, character) in array.iter_mut().enumerate() {

			let x = xor(character.to_string(), matrix[row][column].to_owned());
			*character = x.to_string();

		}

	}

	return data;

}

fn scheduleKey(mut key: Vec<Vec<String>>, round: u8) -> Vec<Vec<String>> {

	*key.last_mut().unwrap() = shuffleVector(key.last().unwrap().clone(), round);
	let mut buffer = vec![];
	let mut matrix: Vec<Vec<String>> = vec![];
	let word = key.last().unwrap().clone();
	let mut vector;

	for (row, array) in key.iter_mut().enumerate() {

		for (column, character) in array.iter_mut().enumerate() {

			let binary = u8::from_str_radix(&character.to_string(), 16).unwrap();
	
			if row == 0 {

				vector = u8::from_str_radix(&word[column].to_owned(), 16).unwrap();

			} else {

				vector = u8::from_str_radix(&matrix.last().unwrap().clone()[column].to_owned(), 16).unwrap();
 
			} 

			let sum = binary ^ vector;
			buffer.push(format!("{:02x}", sum).to_string());

		}

		matrix.push(buffer.clone());
		buffer.clear();

	}

	return matrix;

}

fn sTransform(mut block: Vec<Vec<String>>) -> Vec<Vec<String>> {

	for vector in block.iter_mut() {

		for character in vector.iter_mut() {

			let (row, column) = formatIndex(character.clone());
			*character = constants::sBox.get(&(&row, &column)).unwrap().to_string();

		}

	}

	return block;

}

fn shiftRows(mut block: Vec<Vec<String>>) -> Vec<Vec<String>> {

	let mut buffer = vec![];
	let rows = block.len();

	for position in 1..4 {

		for vector in &block {

			buffer.push(vector[position].to_owned());

		}

		for (index, row) in block.iter_mut().enumerate() {

			if index + position < rows {

				row[position] = buffer[index + position].clone();

			} else {

				row[position] = buffer[position - (rows - 1 - index) - 1].clone();

			}

		}

		buffer.clear();
	
	}
	
	return block;

}

fn mixColumns(block: Vec<Vec<String>>) -> Vec<Vec<String>> {

	let mut matrix = vec![];
	let mut buffer = vec![];
	let mut combination = "00".to_owned();

	for row in block.iter() {

		for vector in constants::mixingMatrix.iter() {

			for (index, column) in row.iter().enumerate() {
				
				let product =
				if vector[index] == "01" {

					column.to_string()

				} else {

					galoiProduct(column.to_string(), vector[index].to_string())

				};

				combination = xor(product, combination);

			}

			buffer.push(combination.to_owned());
			combination = "00".to_owned();

		}

		matrix.push(buffer.clone());
		buffer.clear();

	}

	return block;

}

fn galoiProduct(x: String, y: String) -> String {

	let X = u8::from_str_radix(&x.to_string(), 16).unwrap();
	let Y = u8::from_str_radix(&y.to_string(), 16).unwrap();
	let A = format!("{:08b}", X);
	let B = format!("{:08b}", Y);
	let a = moduloPolynomial(A);
	let b = moduloPolynomial(B);
	let mut c = vec![];

	for i in a.iter() {

		for j in b.iter() {

			if c.contains(&(i + j)) {

				c.retain(|&value| value != i + j);

			} else {

				c.push(j + i);

			}

		}

	}

	if c.contains(&8) {

		c.retain(|&value| value != 8);

		for &k in &[4, 3, 1, 0] {

			if c.contains(&k) {

				c.retain(|&value| value != k);

			} else {

				c.push(k);

			}

		}

	}

	let polynomial = binaryPolynomial(c);
	let decimal = u8::from_str_radix(&polynomial, 2).unwrap();
	let hex = format!("{:02x}", decimal).to_owned();
	return hex;

}

fn moduloPolynomial(word: String) -> Vec<u8> {

	let mut polynomial = vec![];

	for (index, character) in word.chars().enumerate() {

		if character == '1' {

			polynomial.push((word.len() - 1 - index) as u8);

		}

	}

	return polynomial;

}

fn binaryPolynomial(word: Vec<u8>) -> String {

	let mut binary = "00000000".to_owned();

	for index in word.iter() {

		binary.replace_range((binary.len() - 1 - *index as usize)..(binary.len() - *index as usize), "1");

	}

	return binary;

}

fn collapseMatrix(message: Vec<Vec<Vec<String>>>) -> String {

	let mut cipher = String::new();

	for block in message.iter() {

		for row in block.iter() {

			for column in row.iter() {

				cipher.push_str(column);

			}

		}

	}

	return cipher;
}
