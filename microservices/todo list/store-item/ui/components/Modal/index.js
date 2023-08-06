import styles from "./styles.module.css";
import Image from "next/image";


export default function ItemModal({ setVisible }) {

    return (

        <div className={styles.overlay}>

            <form className={styles.modal}
                  onSubmit={(event) => event.preventDefault()}>

                <div className={styles.xButton}>

                    <div className={styles.circle}
                         onClick={() => setVisible(false)}>

                        <Image src="/assets/icons/x.png"
                            width={20}
                            height={20} />

                    </div>

                </div>

                <label className={styles.headingText}>Add a new item to your checklist</label>

                <input className={styles.inputField}
                        placeholder="New item"
                        type="text"/>

                <button className={styles.submitButton}
                        onClick={() => setVisible(false)}>Submit</button>

            </form>

        </div>

    );

}
