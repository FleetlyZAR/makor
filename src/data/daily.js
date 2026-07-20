// Verse of the day rotation. These entries mirror the hand made daily share
// pages under public/daily/. The app picks one per calendar day so that the
// verse in the app matches the daily in rotation for that date. To add a verse
// to the rotation, publish its assets under public/daily/ and add an entry
// here with the same slug.

export const dailyEntries = [
  {
    slug: 'genesis-1-1',
    ref: 'Genesis 1:1',
    verse: 'In the beginning God created the heavens and the earth.',
    story: [
      'Seven Hebrew words open the whole Bible, and everything after them leans back on this one line.',
      'The word for created here is bara. In the Hebrew Scriptures it is a work only ever done by God; no one else is ever its subject. And the name for God, Elohim, is full and majestic. Before the world is set in order, before it falls, before a single promise is made, the first thing we are told is who stands behind it all. He is the source.',
      'This is where Makor begins, because it is where God begins: not with us, but with Him. Come and sit with the beginning.'
    ],
    studyUrl: '/genesis/the-seven-days/'
  },
  {
    slug: 'john-1-1',
    ref: 'John 1:1',
    verse: 'In the beginning was the Word, and the Word was with God, and the Word was God.',
    story: [
      'John opens his Gospel with the very words that open the Bible: in the beginning.',
      'He wants you to hear the echo. The One who spoke the world into being in Genesis is here given a name and a face: the Word, who was with God and was God. The voice at creation was Christ, and nothing that exists came from anywhere else.',
      'The source has a face, and it is Jesus.'
    ],
    studyUrl: '/john/the-word-became-flesh/'
  },
  {
    slug: 'lamentations-3-22',
    ref: 'Lamentations 3:22-23',
    verse: 'Because of the loving devotion of the LORD we are not consumed, for His mercies never fail. They are new every morning; great is Your faithfulness!',
    story: [
      'These famous words were written from the ashes of a fallen city, not from a mountaintop.',
      'The man who wrote them had watched Jerusalem burn. And still he says: the LORD’s mercies never fail; they are new every morning. Not that the pain was small, but that God’s mercy was newer than each day’s grief. Whatever you wake to, His mercy got there first.',
      'This morning, His mercy is new again.'
    ],
    studyUrl: '/lamentations/the-prophets-grief-and-hope/'
  }
];
