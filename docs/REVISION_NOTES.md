# Revision notes

## Version 0.1.1

The manuscript defines G_p(t) directly from binomial coefficients and Q_n,
and uses G_p(-1/32) and G_p(1/64) throughout. The abbreviations g_n, S_-(p)
and S_+(p) have been removed. The infinite period G(t) is retained for the
modular argument.

Section 4 now explicitly credits Mao's stronger Q_np congruence and explains
its relation to the known endpoint needed modulo p². The proof using Straub
and Gorodetsky remains, including its coverage of p=3. The degree-p comparison
in Section 8 is explicitly attributed to the proof of Beukers' Theorem 6.1.
An acknowledgment thanks Zhi-Hong Sun for his comments and source pointer.
The AI-use disclosure is retained.

The main theorem, its domain, the mathematical arguments and the finite
computational results are unchanged. The scientific code, tests and six
supplied JSON evidence files are unchanged. The evidence inventory has a new
digest because VERSION is one of its declared members. Historical JSON keys
such as `gp` still mean `binom(2p,p) Q_p`; changing paper notation does not
change their schema.

The revision was checked by an AI system with access to the prior work.
Computational replay and manuscript review do not constitute independent
specialist refereeing, formal verification or a determination of priority.
