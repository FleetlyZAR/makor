# Issues agents found in frozen (basic level) content

Deepening agents may not edit the basic level, lexicon or passage text. When
they notice a problem there, it is logged here for a separate, human-approved fix.

- exodus/08-aarons-staff-becomes-a-serpent.json: the lexicon token in the basic text implies chazaq for Exodus 7:3, but 7:3 uses qashah (7:13 uses chazaq).
- exodus/46-the-sabbath-and-the-offering.json: the lexicon entry 'ability' (and basic originalLanguages) gives the lemma horaah for Exodus 35:34, but the verse uses the Hiphil infinitive of yarah (ul'horot, 'to teach'); horaah is a later, post-biblical noun.
- leviticus/01-the-burnt-offering.json: study.basic.originalLanguages says kaphar "describes the laying on of hands"; the hand-laying verb in 1:4 is samakh, while kaphar (kipper) is the verb "make atonement".
- leviticus/03-the-peace-offering.json: translationNotes on 3:17 says chuqqat olam distinguishes this rule "from ceremonial regulations tied specifically to the tabernacle and priesthood"; the same phrase is used of tabernacle rites (for example Leviticus 16:29, 16:34, 24:3), so the contrast does not hold.
- leviticus/05-the-guilt-offering.json: study.basic.context says the guilt offering 'always comes with restitution' and the asham lexicon gloss says it requires restitution, but Leviticus 5:17-19 prescribes a guilt offering ram with no restitution or added fifth.
- leviticus/14-cleansing-of-skin-diseases-and-mildew.json: the basic originalLanguages and the lexicon gloss for ezov quote Psalm 51:7 as 'purge me with hyssop', but the BSB reads 'Purify me with hyssop'.
- leviticus/23-the-appointed-feasts.json: the {{bikkurim|firstfruits}} token sits on Leviticus 23:10, where the Hebrew is reshit (the first of your harvest); bikkurim occurs in 23:17 and 23:20. The bikkurim lexicon gloss also says Paul uses 'this exact term' in 1 Corinthians 15:20, but Paul's Greek word is aparche.
- numbers/23-the-oracles-of-balaam.json study.basic.originalLanguages: says "God has received a command to barak, bless"; in Numbers 23:20 it is Balaam who has received the command to bless, not God.
- numbers/22-balaam-and-the-donkey.json study.basic.crossReferences: says 2 Peter 2:15-16 and Jude 11 both use the donkey's rebuke; only 2 Peter mentions the donkey, Jude 1:11 does not.
- deuteronomy/14-clean-food-and-tithes.json: the lexicon entry keyed tahor (the token {{tahor|unclean}} in verse 7) has lemma tame and gloss 'Unclean'; tahor means clean, so the key does not match the lemma or the word it marks.
- numbers/25-the-sin-at-peor.json: study.basic.typology describes Phinehas as 'standing between the living and the dying'; that phrase belongs to Aaron in Numbers 16:48, not to Phinehas in Numbers 25.
- deuteronomy/03-the-conquest-of-bashan.json: study.basic.originalLanguages and the nachalah lexicon entry say the eastern tribes' land in Deuteronomy 3 is called their nachalah, but the noun does not occur in chapter 3; their land is their yerushah ('possession', 3:20), and the related verb nachal appears only in 3:28 ('enable them to inherit'). nachalah itself first appears in 4:21 and 4:38.
- deuteronomy/05-the-ten-commandments-restated.json: the panim lexicon entry (and study.basic.originalLanguages) gives the phrase in 5:4 as panim el panim; the Hebrew of Deuteronomy 5:4 reads panim be-panim ('face in face'). panim el panim is the wording used of Moses in Exodus 33:11 and Deuteronomy 34:10.
