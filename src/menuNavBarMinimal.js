import { mdiAccount, mdiLogout, mdiSwapHorizontal, mdiCart } from '@mdi/js'

export default [
  {
    icon: mdiSwapHorizontal,
    label: 'Historique Mouvement',
    to: '/historiques-mouvements',
  },
  {
    icon: mdiCart,
    label: 'Historique Vente',
    to: '/historique-ventes',
  },
  {
    isCurrentUser: true,
    menu: [
      {
        icon: mdiAccount,
        label: 'Mon Profil',
        to: '/profile',
      },
      {
        isDivider: true,
      },
      {
        icon: mdiLogout,
        label: 'Déconnexion',
        isLogout: true,
      },
    ],
  },
]
